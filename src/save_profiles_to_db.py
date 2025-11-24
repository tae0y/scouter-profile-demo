import json
import psycopg2
import os


def to_param_str(param):
    if param is None:
        return None
    if isinstance(param, (dict, list)):
        return json.dumps(param, ensure_ascii=False)

def to_param_str(param):
    if param is None:
        return None
    if isinstance(param, (dict, list)):
        return json.dumps(param, ensure_ascii=False)
    return str(param)
def save_profiles(json_path, db_params):
    print("=== save_profiles 진입 ===")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            print(f"파일 열림: {json_path}")
            profiles = json.load(f)
        print(f"profiles 데이터 개수: {len(profiles)}")
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        row_count = 0
        for item in profiles:
            txid = item.get("txid")
            print(f"txid: {txid}")
            steps = item.get("profile", [])
            print(f"steps 개수: {len(steps)}")
            for step in steps:
                main_value = step.get("mainValue", None)
                step_info = step.get("step", {})
                if not isinstance(step_info, dict):
                    step_info = {}
                step_index = step_info.get("index", None)
                start_time = step_info.get("start_time", None)
                start_cpu = step_info.get("start_cpu", None)
                elapsed = step_info.get("elapsed", None)
                cputime = step_info.get("cputime", None)
                step_type = step_info.get("stepType", None)
                step_order = step_info.get("order", None)
                step_type_name = step_info.get("stepTypeName", None)
                param = to_param_str(step_info.get("param", None))
                params = [
                    txid,
                    main_value,
                    step_index,
                    start_time,
                    start_cpu,
                    elapsed,
                    cputime,
                    step_type,
                    step_order,
                    step_type_name,
                    param
                ]
                print("PARAMS 개수:", len(params), params)
                cur.execute(
                    "INSERT INTO profiles (txid, main_value, step_index, start_time, start_cpu, elapsed, cputime, step_type, step_order, step_type_name, param) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    params
                )
                row_count += 1
        conn.commit()
        cur.close()
        conn.close()
        print(f"Saved {row_count} profile steps to DB.")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    print("save_profiles_to_db started!!")
    db_params = {
        "host": os.getenv("PGHOST", "localhost"),
        "port": os.getenv("PGPORT", "5432"),
        "dbname": os.getenv("PGDATABASE", "profilesdb"),
        "user": os.getenv("PGUSER", "profileuser"),
        "password": os.getenv("PGPASSWORD", "profilepass"),
    }
    save_profiles("profiles.json", db_params)
