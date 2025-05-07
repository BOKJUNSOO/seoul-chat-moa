from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import psycopg2
import pandas as pd

# paring input!
import re

SEOUL_DISTRICTS = [
    "종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구",
    "성북구", "강북구", "도봉구", "노원구", "은평구", "서대문구", "마포구",
    "양천구", "강서구", "구로구", "금천구", "영등포구", "동작구", "관악구",
    "서초구", "강남구", "송파구", "강동구"
]

def parse_user_input(text: str):    
    station_match = re.search(r"([가-힣]+역)", text)
    gu_match      = re.findall(r"([가-힣]+구)", text)
    
    gu = None
    for candidate in gu_match:
        if candidate in SEOUL_DISTRICTS:
            gu = candidate
            break

    category_keywords = ['연극', '클래식', '축제', '교육', '체험', '미술전시', '콘서트', '영화', '국악','뮤지컬', '오페라', '무용', '기타', '독주', '독창회']
    
    keywords=[]
    for keyword in category_keywords:
        if keyword in text:
            keywords.append(keyword)

    return {
        "station": station_match.group(1) if station_match else None,
        "gu":           gu,
        "keywords":keywords
    }

def build_meta_filter(parsed: dict):
    filters = []
    for k in ("station", "gu"):
        if parsed.get(k):
            filters.append({k: parsed[k]})
    
    if parsed.get("keywords"):
        for keyword in parsed["keywords"]:
            filters.append({"category": keyword})

    if not filters:
        return {}
    if len(filters) == 1:
        return filters[0]

    return {"$and": filters}


conn_params = {
        "host": "host.docker.internal",
        "port": 15432,
        "dbname": "seoulmoa",
        "user": "airflow",
        "password": "airflow"
    }


def fetch_additional_data(event_id: int,id:int) -> dict:
    """
    event_id를 기반으로 다른 DB에서 가져올 칼럼을 쿼리합니다.
    예) organizer, price, tickets_available 등
    """
    try:
        # connect
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()

        # search db
        cur.execute("SELECT current_database(), current_schema();")
        #db, schema = cur.fetchone()

        # schema list
        cur.execute("SELECT schema_name FROM information_schema.schemata;")
        #schemata = [row[0] for row in cur.fetchall()]

        # st search_path
        cur.execute("SET search_path TO datawarehouse;")

        # search table
        cur.execute("""
          SELECT table_name
          FROM information_schema.tables
          WHERE table_schema = 'datawarehouse';
        """)

        # read member_event
        member_event = pd.read_sql_query("""SELECT count(*) AS cnt FROM "member_event" WHERE event_id = %s""",
                                         conn,
                                         params=[event_id])
        likeCount = member_event.iloc[0,0]

        member_if = pd.read_sql_query("""SELECT 1 FROM "member_event" where event_id =%s AND member_id=%s""",
                                      conn,
                                      params=[event_id,id])

        isLiked: bool = not member_if.empty
    
    except psycopg2.Error as e:
        print(e)
        raise
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

    # 반환 형태 예시
    return {
        "likeCount":likeCount,
        "isLiked":isLiked
    }
