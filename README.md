<div align="center">
   <h1> 서울모아 </h1>
   <h3> 챗봇 MOA </h3>
   <h3> Langchain Application with FastAPI</h3>
</div>

## 📢 프로젝트 소개

`#FastAPI` `#LangChain` `#ChatBot` `#Embedding` `#RAG`

서울모아의 데이터 파이프라인으로 부터 수집된 행사정보를 이용하여 파인튜닝한 챗봇입니다.<br>



## 🔎 주요 기능 소개


### 🎯 위치 기반 검색 기능 및 행사 카테고리별 추천 기능
사용자 입력에 대하여 특정 행정구역, 지하철역, 카테고리 키워드를 파싱한후 적절한 행사 정보를 제공합니다.

<div style="display: flex; gap: 1rem; justify-content: center;">
  <figure style="margin: 0; text-align: center;">
    <img height="400" src="https://github.com/user-attachments/assets/56e9cb9b-01d3-4274-a56a-013dc9ac9b49">
    <figcaption style="font-size: 0.8rem; color: #666; margin-top: 0.5rem;">
      사용자가 입력한 '왕십리역'과 '콘서트' 대한 질의
    </figcaption>
  </figure>
  <figure style="margin: 0; text-align: center;">
    <img height="400" 
    src="https://github.com/user-attachments/assets/2b247d54-3e67-40c9-b199-a5f68547e20c">
    <figcaption style="font-size: 0.8rem; color: #666; margin-top: 0.5rem;">
      실제 챗봇이 찾아온 행사 정보
    </figcaption>
  </figure>
</div>



### 🎯 사용자 입력에 대한 응답과 공감

특정 지역에 대한 검색이 아니라 할지라도 맥락을 고려한 응답을 해준다는 특징이 있습니다.

특정 카테고리를 검색하는 것에는 실패했을지라도 임베딩된 DB에서 데이터를 무조건적으로 검색해옵니다.

<div style="display: flex; gap: 1rem; justify-content: center;">
  <!-- 🎯 사용자 입력에 대한 응답 -->
  <figure style="margin: 0; text-align: center;">
    <img height="400"
      src="https://github.com/user-attachments/assets/a71b5bed-9616-49e2-baf0-5f1dca38580d"
      style="max-width: 100%; height: auto; display: block; margin: 0 auto;">
    <figcaption style="font-size: 0.8rem; color: #666; margin-top: 0.5rem;">
      '바이올린'이라는 사용자 입력에 대한 응답 예시
    </figcaption>
  </figure>
  <figure style="margin: 0; text-align: center;">
    <img height="400"
      src="https://github.com/user-attachments/assets/2dd00a21-ee12-487f-b4cc-73e42599af8d"
      style="max-width: 100%; height: auto; display: block; margin: 0 auto;">
    <figcaption style="font-size: 0.8rem; color: #666; margin-top: 0.5rem;">
      행사정보와 무관한 요청을 보냈을때
    </figcaption>
  </figure>
</div>

## ⚒️ 기술 스택

| 분류 | 기술 |
| ---- | ---- |
| 언어 | <img src= "https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"> |
| 사용 라이브러리 |  <img src="https://img.shields.io/badge/openai-412991?style=flat-square&logo=openai&logoColor=white"> <img src="https://img.shields.io/badge/langchain--community-000000?style=flat-square&logo=LangChain&logoColor=white">  <img src="https://img.shields.io/badge/psycopg2-2c5d85?style=flat-square&logo=postgresql&logoColor=white"> <img src="https://img.shields.io/badge/sqlalchemy-336791?style=flat-square&logo=SQLAlchemy&logoColor=white"> <img src="https://img.shields.io/badge/geopy-000000?style=flat-square&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/tiktoken-000000?style=flat-square&logo=python&logoColor=white"> |
| 백엔드 | <img src="https://img.shields.io/badge/fastapi-009688?style=flat-square&logo=fastapi&logoColor=white"> <img src="https://img.shields.io/badge/uvicorn-222222?style=flat-square&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/ChromaDB-20232a?style=flat-square&logo=chroma&logoColor=white">|
| 배포 | <img src= "https://img.shields.io/badge/Jenkins-D24939?style=flat-square&logo=jenkins&logoColor=white"> <img src= "https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white"> |

## 🏆 Seoul-moa 팀원 깃허브

<table align="center" width="100%">
  <tr>
    <td><img src="https://avatars.githubusercontent.com/u/68840464?v=4"/></td>
    <td><img src="https://avatars.githubusercontent.com/u/102515499?v=4"/></td>
    <td><img src="https://avatars.githubusercontent.com/u/108779266?v=4"/></td>
    <td><img src="https://avatars.githubusercontent.com/u/73154551?v=4"/></td>
    <td><img src="https://avatars.githubusercontent.com/u/170912062?v=4"/></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/Hwanjin-Choi">최환진</a>
    </td>
    <td align="center"><a href="https://github.com/seoyoun8694">채서윤</a>
    </td>
    <td align="center"><a href="https://github.com/SoonWookHwang">황순욱</a>
    </td>
    <td align="center"><a href="https://github.com/MingyooLee">이민규</a>
    </td>
    <td align="center"><a href="https://github.com/BOKJUNSOO">복준수</a>
  </tr>
  <tr>
    <td align="center">Front-End</td>
    <td align="center">Front-End</td>
    <td align="center">Back-End</td>
    <td align="center">Back-End & Deploy</td>
    <td align="center">Data Engineering</td>
  </tr>
</table>

## 🎈 Project repo

[프론트엔드 서버 레포는 여기!](https://github.com/Hwanjin-Choi/project-seoul-moa-frontend)

[백엔드 서버 레포는 여기!](https://github.com/SoonWookHwang/seoul-moa)

[데이터 파이프라인 서버는 여기!](https://github.com/BOKJUNSOO/seoul-de)

[chat moa 서버는 여기!](https://github.com/BOKJUNSOO/seoul-chat-moa)

<br>

## 🔥 Data Engineering 에서의 도전 과제

```
세부적인 내용은 아래 링크의 velog 링크에서 확인할 수 있습니다!
```

1. RAG에서 Retrieval 전략 `코드레벨`\
[작성중..](https://velog.io/@junsoobok/posts)
- 데이터 노이즈
- 사용자 입력의 예측

2. embedding! `코드 레벨`\
[작성중..](https://velog.io/@junsoobok/posts)

3. FastAPI`(인프라레벨)`\
[작성중..](https://velog.io/@junsoobok/posts)


## 😎 프로젝트 실행

### port info

FastAPI SERVER : 8001\
Chroma DB : 8000

### project run

```bash
git clone https://github.com/BOKJUNSOO/seoul-chat-moa
docker compose up --build -d
```

## 😎 프로젝트 사용시 설정사항

- OPEN AI 키 발급
- `.env.compose` 파일을 프로젝트 디렉토리에 추가

### openai key

`.env.compose` 파일에 발급받은 키를아래와 같이 기입합니다.
```
OPENAI_API_KEY='YOUR OPEN AI API KEY'
```

### 빌드후 임배딩 과정이 필요합니다.

- 초기 데이터셋은 `seoul-de`를 통해 구축해야 합니다.
  >해당 레포를 확인 ↓\
  >[seoul-de](https://github.com/BOKJUNSOO/seoul-de)

- 최초 1회 자동으로 이루어 지는 과정이지만 시간이 조금 걸립니다(1분).
- 터미널창에서 다음 메세지가 나오면 서버 빌드가 끝난 상태입니다.
- 해당 로그 이후에 컨테이너 3개중 2개만 작동되고 있는게 정상인 상태입니다.

```bash
# 터미널창에서 확인할 로그
...
festivalbot-api  | INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
embedder         | [INFO] embedding task is done !
embedder         | [INFO] do not restart this container
embedder         | [INFO] You can use moa chat service
```

- 컨테이너를 다시 빌드하면 임베딩 과정을 다시 진행합니다.
    >docker compose file에서 embedding 컨테이너를 주석처리 해주세요.\
    >임베딩시 추가 토큰 비용이 발생합니다.
    >
    >임베딩을 1회 진행했다면 `chroma_data`가 로컬에 마운트 되어 생성되어 있습니다.\
    >이를 이용하면 되므로 추가적인 임베딩은 필요하지 않습니다.
```yaml
#   embedder:
#     build:
#       context: ./core
#       dockerfile: Dockerfile
#     container_name: embedder
#     env_file:
#       - .env.compose
#     volumes:
#       - ./chroma_data:/embedding/chroma_data
#       - ./core:/app/core
#     command: python embedding.py
#     restart: "no"
```

