import re

SEOUL_DISTRICTS = [
    "종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구",
    "성북구", "강북구", "도봉구", "노원구", "은평구", "서대문구", "마포구",
    "양천구", "강서구", "구로구", "금천구", "영등포구", "동작구", "관악구",
    "서초구", "강남구", "송파구", "강동구"
]

category_keywords = ['연극', '클래식', '축제', '교육', '체험', '미술전시', '콘서트', '영화', '국악','뮤지컬', '오페라', '무용', '기타', '독주', '독창회']

def parse_user_input(text: str):    
    gu_match      = re.findall(r"([가-힣]+구)", text)
    station_match = re.search(r"([가-힣]+역)", text)

    keywords=[]
    for keyword in category_keywords:
        if keyword in text:
            keywords.append(keyword)
    
    gu = None
    for candidate in gu_match:
        if candidate in SEOUL_DISTRICTS:
            gu = candidate
            break
    
    is_fee =None
    if "무료" in text:
        is_fee = "무료"
    
    return {
        "station": station_match.group(1) if station_match else None,
        "gu":           gu,
        "keywords":keywords,
        "is_free": is_fee
    }

def build_meta_filter(parsed: dict):
    filters = []
    for k in ("station", "gu"):
        if parsed.get(k):
            filters.append({k: parsed[k]})
    
    if parsed.get("keywords"):
        for keyword in parsed["keywords"]:
            filters.append({"category": keyword})
    
    if parsed.get("is_free"):
        filters.append({"is_free": parsed["is_free"]})

    if not filters:
        return {}
    
    if len(filters) == 1:
        return filters[0]

    return {"$and": filters}
