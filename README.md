# README

## Getting Started

1. Python 가상환경을 생성하고 패키지 설치를 설치합니다.

    ```bash
    uv sync
    .venv/bin/activate # Mac/Linux
    ```

1. `.env` 파일에 webapp 도메인 주소와 추출할 날짜, 시간 등을 입력합니다.

    ```
    BASE_URL=http://{SCOUTER_WEBAPP_DOMAIN}:{SCOUTER_WEBAPP_PORT}
    DATE=20251124
    START_HMS=080000
    END_HMS=170000
    OUTPUT_PATH=profiles.json
    ```
    > Scouter webapp 기동방법은 다음 문서를 참고하세요 👉 [Web API Guide](https://github.com/scouter-project/scouter/blob/master/scouter.document/tech/Web-API-Guide.md) 

1. 컨테이너를 띄우기 전에 dbadmin의 권한 설정을 해줍니다.
    ```bash
    mkdir -p docker/volumes/pgadmin
    chown -R 5050:5050 docker/volumes/pgadmin
    chmod -R 700 docker/volumes/pgadmin
    ```

1. 컨테이너로 데이터를 저장할 db, 데이터 조회시 사용할 dbadmin을 기동합니다.

    ```bash
    cd docker
    docker compose up -d --build
    ```

1. 스크립트를 실행해 프로파일 데이터를 수집하고 파일로 저장합니다.

    ```bash
    cd src
    uv run main.py
    ```

1. 스크립트를 실행해 DB에 데이터를 저장합니다.

    ```bash
    cd src
    uv run save_profiles_to_db.py
    ```

1. dbadmin에 접속해서 데이터를 조회하고 활용합시다!
    > Admin 접속주소: `http://localhost:8080`\
    > Admin 계정정보: `admin@local.com` / `adminpass`\
    > DB 접속주소: `db`\
    > DB명: `profilesdb`\
    > DB 계정정보: `profileuser` / `profilepass`

    ```sql
    # DB 쿼리
    SELECT txid, elapsed, main_value, param
    FROM public.profiles
    WHERE step_type_name = 'SQL3'
    ORDER BY elapsed DESC
    ```
    ```sql
    # 메서드
    SELECT txid, elapsed, REPLACE(REPLACE(main_value, CHR(10), ''), CHR(13), ''), param
    FROM public.profiles
    WHERE step_type_name = 'METHOD'
    ORDER BY elapsed DESC
    ```
    > Scouter를 활용한 메서드 프로파일링 방법은 다음 문서를 참고하세요 👉 [Method Profiling](https://github.com/scouter-project/scouter/blob/master/scouter.document/use-case/Method-Profiling.md)

    각 데이터 필드는 다음과 같습니다.
    - txid : 트랜잭션 ID
    - elapsed : 밀리초 단위 소요시간
    - main_value : SQL 쿼리 문자열 혹은 Java 메서드명
    - param : SQL 쿼리의 파라미터
