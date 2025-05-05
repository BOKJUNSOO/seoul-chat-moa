# SETTING


- `.env.compose` 파일을 프로젝트 디렉토리에 추가
```
# openai key
OPENAI_API_KEY='YOUR OPEN AI API KEY'
```

# Project run
```bash
docker compose up --build --remove-orphans
```

## 빌드후 임배딩 과정이 필요합니다.
- 자동으로 이루어 지는 과정이지만 시간이 조금 걸립니다(1분).
- 터미널창에서 다음 메세지가 나오면 서버 빌드가 끝난 상태입니다.
- 해당 로그 이후에 컨테이너 3개중 2개만 작동되고 있는게 정상인 상태입니다.

```bash
...
festivalbot-api  | INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
embedder         | [INFO] embedding task is done !
embedder         | [INFO] do not restart this container
embedder         | [INFO] You can use moa chat service
```
