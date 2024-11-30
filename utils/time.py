from datetime import datetime, timezone, timedelta

def convert_to_kst(utc_timestamp: str) -> str:
    # 슬랙 타임스탬프를 float로 변환
    utc_time = datetime.fromtimestamp(float(utc_timestamp), tz=timezone.utc)
    # UTC+9 (KST)로 변환
    kst_time = utc_time.astimezone(timezone(timedelta(hours=9)))
    # KST 시간 문자열로 변환 (YYYY-MM-DD HH:MM:SS)
    return kst_time.strftime("%Y-%m-%d %H:%M:%S")

