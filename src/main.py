import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

BASE_URL = os.getenv("BASE_URL")
DATE = os.getenv("DATE")
START_HMS = os.getenv("START_HMS")
END_HMS = os.getenv("END_HMS")
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "profiles.json")

def get_object_hashes():
    url = f"{BASE_URL}/scouter/v1/object"
    resp = requests.get(url)
    resp.raise_for_status()
    objects = resp.json()["result"]
    return [obj['objHash'] for obj in objects]

def get_xlogs(date, start_hms, end_hms, obj_hashes):
    obj_hash_str = ",".join(map(str, obj_hashes))
    url = f"{BASE_URL}/scouter/v1/xlog/{date}?startHms={start_hms}&endHms={end_hms}&objHashes={obj_hash_str}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()["result"]["xlogs"]

def get_profile_data(date, txid):
    url = f"{BASE_URL}/scouter/v1/profile-data/{date}/{txid}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()["result"]

if __name__ == "__main__":
    obj_hashes = get_object_hashes()
    xlogs = get_xlogs(DATE, START_HMS, END_HMS, obj_hashes)

    all_profiles = []
    for xlog in xlogs:
        txid = xlog.get("txid")
        if txid:
            profile = get_profile_data(DATE, txid)
            all_profiles.append({"txid": txid, "profile": profile})
            print(f"txid: {txid}, profile: {profile}")

    # 결과를 파일로 저장
    import json
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_profiles, f, ensure_ascii=False, indent=2)
