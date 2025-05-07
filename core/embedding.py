# Embedding task!
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
import json
import tiktoken
import pandas as pd
import os
import psycopg2
import warnings
from datetime import datetime
from geopy.distance import geodesic

warnings.filterwarnings('ignore')
def get_nearest_station(event_lat, event_lon, stations_df):
    # 모든 역과의 거리 계산
    stations_df["distance_km"] = stations_df.apply(
        lambda row: geodesic((event_lat, event_lon), (row["latitude"], row["longitude"])).km, axis=1
    )
    # 가장 가까운 역 반환
    nearest = stations_df.loc[stations_df["distance_km"].idxmin()]
    return nearest["name"]

# category_name에 '/'가 포함된 경우 처리하는 함수
def expand_category(df):
    expanded_rows = []
    
    # 원본 데이터에서 각 행을 처리
    for _, row in df.iterrows():
        categories = row['category_name'].split('/')  # '/' 기준으로 분리
        for category in categories:
            new_row = row.copy()  # 기존 행 복사
            new_row['category_name'] = category  # category_name을 새로 설정
            expanded_rows.append(new_row)  # 새로운 행 추가
    
    return pd.DataFrame(expanded_rows)  # 새로운 DataFrame 반환

# 토큰 수 계산 및 분할 함수 정의
def chunk_text_by_tokens(text, max_tokens=2000, model_name="text-embedding-ada-002"):
    """주어진 텍스트를 모델의 최대 토큰 수 단위로 분할"""
    encoder = tiktoken.encoding_for_model(model_name)
    tokens = encoder.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk = tokens[i:i+max_tokens]
        chunks.append(encoder.decode(chunk))
    return chunks

if __name__=='__main__':
    # connect to data base
    conn_params = {
        "host": "host.docker.internal",
        "port": 15432,
        "dbname": "seoulmoa",
        "user": "airflow",
        "password": "airflow"
    }

    try:
        # connect
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()

        # search db, schema
        cur.execute("SELECT current_database(), current_schema();")
        db, schema = cur.fetchone()

        # schema list
        cur.execute("SELECT schema_name FROM information_schema.schemata;")
        schemata = [row[0] for row in cur.fetchall()]

        # st search_path
        cur.execute("SET search_path TO datawarehouse;")

        # search table
        cur.execute("""
          SELECT table_name
          FROM information_schema.tables
          WHERE table_schema = 'datawarehouse';
        """)

        # 지하철 마스터정보
        stations = pd.read_sql_query(f'SELECT * FROM "subway_station"', conn)
        stations = stations.drop(columns=['line'])
        stations = stations.drop_duplicates(subset='name').reset_index(drop=True)
    except psycopg2.Error as e:
        print(e)
        raise
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
    try:
        # connect
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()

        # search db, schema
        cur.execute("SELECT current_database(), current_schema();")
        db, schema = cur.fetchone()

        # schema list
        cur.execute("SELECT schema_name FROM information_schema.schemata;")
        schemata = [row[0] for row in cur.fetchall()]

        # st search_path
        cur.execute("SET search_path TO datawarehouse;")

        # search table
        cur.execute("""
          SELECT table_name
          FROM information_schema.tables
          WHERE table_schema = 'datawarehouse';
        """)

        # 행사 정보
        events = pd.read_sql_query(f'SELECT * FROM "event"', conn)
    except psycopg2.Error as e:
        print(e)
        raise
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

    # refine
    today_ = datetime.today().strftime("%Y-%m-%d")
    events = events[events["end_date"] >= today_].reset_index(drop=True)
    events['start_date']=pd.to_datetime(events['start_date'])
    events['end_date']=pd.to_datetime(events['end_date'])

    answer = []
    length_ = len(events)
    
    for i in range(0,length_):
        a = get_nearest_station(events['latitude'][i], events['longitude'][i], stations) # 바꿔야함!
        answer.append(a)
    
    events['near_station'] = answer

    events['start_date'] = pd.to_datetime(events['start_date'])
    events['end_date'] = pd.to_datetime(events['end_date'])

    events['station'] = events['near_station'].str.extract(r'^([^\(]+)')  # 괄호 앞 텍스트
    events['sub'] = events['near_station'].str.extract(r'\(([^)]+)\)')  # 괄호 안 텍스events
    
    events['sub']=events['sub'].fillna("")
    events['location'] = events['location'] + "-" + events['sub']
    events = events[["event_id","title","is_free","category_name","gu","location","start_date","end_date","target_user","event_description","station"]]
    
    events.to_csv("./event_.csv")
    # now embedding task
    df = events
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])

    expanded_df = expand_category(df)
    expanded_df.category_name.unique()
    expanded_df['category_name'] = expanded_df['category_name'].replace({'미술':'미술전시','전시':'미술전시'})
    expanded_df = expanded_df.drop_duplicates(subset='event_id', keep='first')

    # 데이터프레임을 문서 리스트로 변환하며 텍스트 분할
    documents = []
    for _, row in expanded_df.iterrows():
        payload = {
            "title": row["title"],
            "is_free": row["is_free"],
            "category": row["category_name"],
            "gu": row["gu"],
            "location": f"{row['location']}",
            "start_date": row["start_date"].strftime("%Y-%m-%d"),
            "end_date": row["end_date"].strftime("%Y-%m-%d"),
            "target_user": row["target_user"],
            "station":row["station"]
        }

        text = json.dumps(payload, ensure_ascii=False)

        # 텍스트를 토큰 단위로 분할하여 여러 Document 생성
        text_chunks = chunk_text_by_tokens(text)
        for part in text_chunks:
            documents.append(
                Document(
                    page_content=part,
                    metadata={
                        "event_id": str(row["event_id"]),
                        "title": row["title"],
                        "category": row["category_name"],
                        "location": f"{row['location']}",
                        "gu": row["gu"],
                        "station":row["station"],
                        "start_date": str(row["start_date"].date()),
                        "end_date": str(row["end_date"].date())
                    }
                )
            )

    # 임베딩 및 벡터 DB 초기화
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(
        embedding_function=embeddings,
        persist_directory="/embedding/chroma_data",
        collection_name="event_data"
    )

    # 배치 크기를 설정하여 add_documents 반복
    batch_size = 100
    for i in range(0, len(documents), batch_size):
        batch = documents[i : i + batch_size]
        vectordb.add_documents(batch)

    # 최종 persist 호출
    vectordb.persist()
    print("[INFO] embedding task is done !")
    print("[INFO] do not restart this container")
    print("[INFO] You can use moa chat service")

