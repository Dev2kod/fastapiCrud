import re
from difflib import get_close_matches

#violation type returned as helmet, jacket
# time returned as today, yesterday, last_7_days, last_3_months, last_1_year, 3_days_ago, 2_months_ago, 1_year_ago, last_30_minutes, last_2_hours, 15_minutes_ago, 1_hour_ago



def parseQuery(query:str):
    # Converts user query into structured format
    # Handles:
    # - camera detection (safe, context-aware)
    # - severity
    # - status
    # - violation type (basic fuzzy)
    # - time (today, yesterday, X days ago)
    
    
    queryLower = query.lower()
    print(f"queryLower : {queryLower}")
    
    parsed = {
        "camera_id": None,
        "severity": None,
        "violation_type": None,
        "site": None,
        "time": None,
        "sort": None,
        "text": query
    }
    
    parsed["camera_id"] = extract_camera_id(queryLower)

        
    #word to number regex query, camera one camera two
    
    word_to_number = {
        "one": 1, "two": 2, "three": 3, "four":4, "five":5,
        "first": 1, "second": 2, "third": 3, "fourth":4, "fifth":5
    }
    
    for word, num in word_to_number.items():
        if re.search(rf'(camera|cam).*(\b{word}\b)',queryLower) or\
            re.search(rf'(\b{word}\b).*(camera|am)',queryLower):
                parsed["camera_id"] = num

    #ordinal 
    ordinalMatch = re.search(r'(\d+)(st|nd|th|rd)\s*(camera|cam)',queryLower)
    if ordinalMatch:
        parsed["camera_id"]=int(ordinalMatch.group(1))
        
    #------------------    
    #severity catching
    #------------------
    severityMatching={
        "highest":"High","mid":"Medium","lowest":"Low",
        "higher":"High","mid level":"Medium","lower":"Low",
        "high":"High","medium":"Medium","low":"Low"
    }
    
    for word, severity in severityMatching.items():
        if word in queryLower:
            parsed["severity"] = severity
            break   # stop after first match


            
            
    # -----------------------------
    #  STATUS
    # -----------------------------

    if "active" in queryLower:
        parsed["status"] = "Active"
    elif "closed" in queryLower:
        parsed["status"] = "Closed"
        
    #------------------ 
    #violation type
    #------------------
    
    violationKeywords = {
        "jacket": "Reflective Jackets",
        "vest": "Reflective Jackets",
        "helmet": "Helmet",
        "head" : "Helmet",
        "cap": "Helmet",
        "headgear":"Helmet"
    }
    
    words = queryLower.split()
    
    for word in words:
        match = get_close_matches(word, violationKeywords.keys(), n=1, cutoff=0.7)
        if match:
            parsed["violation_type"] = violationKeywords[match[0]]
        
            # -----------------------------
    # 🧠 7. TIME (today, yesterday)
    # -----------------------------
    # -----------------------------
    # 10. TIME (recent / latest)
    # -----------------------------

    if "recent" in queryLower or "latest" in queryLower:
        parsed["time"] = "recent"
        parsed["sort"] = "desc"

    if "oldest" in queryLower:
        parsed["sort"] = "asc"
    if "today" in queryLower:
        parsed["time"] = "today"

    elif "yesterday" in queryLower:
        parsed["time"] = "yesterday"

    # -----------------------------
    # 8. TIME (last X days / past X days)
    # -----------------------------

    last_days_match = re.search(r'(last|past)\s*(\d+)\s*day[s]?', queryLower)
    if last_days_match:
        parsed["time"] = f"last_{last_days_match.group(2)}_days"

    # -----------------------------
    # 8. TIME (last X months / past X months)
    # -----------------------------

    last_months_match = re.search(r'(last|past)\s*(\d+)\s*month[s]?', queryLower)
    if last_months_match:
        parsed["time"] = f"last_{last_months_match.group(2)}_months"

    # -----------------------------
    # 8. TIME (last X years / past X years)
    # -----------------------------

    last_yrs_match = re.search(r'(last|past)\s*(\d+)\s*year|yr[s]?', queryLower)
    if last_yrs_match:
        parsed["time"] = f"last_{last_yrs_match.group(2)}_years"

    # -----------------------------
    # 8. TIME (last X mins / past X mins)
    # -----------------------------

    last_mins_match = re.search(r'(last|past)\s*(\d+)\s*min|minute[s]?', queryLower)
    if last_mins_match:
        parsed["time"] = f"last_{last_mins_match.group(2)}_minutes"

    # -----------------------------
    # 8. TIME (last X hrs / past X hrs)
    # -----------------------------

    last_hrs_match = re.search(r'(last|past)\s*(\d+)\s*hr|hour[s]?', queryLower)
    if last_hrs_match:
        parsed["time"] = f"last_{last_hrs_match.group(2)}_hours"

    # -----------------------------
    # 9. TIME (X days ago / before)
    # -----------------------------

    days_ago_match = re.search(r'(\d+)\s*day[s]?\s*(ago|before)', queryLower)
    if days_ago_match:
        parsed["time"] = f"{days_ago_match.group(1)}_days_ago"
        
    # -----------------------------
    # 9. TIME (X months ago / before)
    # -----------------------------

    months_ago_match = re.search(r'(\d+)\s*month[s]?\s*(ago|before)', queryLower)
    if months_ago_match:
        parsed["time"] = f"{months_ago_match.group(1)}_months_ago"

    # -----------------------------
    # 9. TIME (X years ago / before)
    # -----------------------------

    years_ago_match = re.search(r'(\d+)\s*(year|yr)[s]?\s*(ago|before)', queryLower)
    if years_ago_match:
        parsed["time"] = f"{years_ago_match.group(1)}_years_ago"

    # -----------------------------
    # 9. TIME (X minutes ago / before)
    # -----------------------------

    mins_ago_match = re.search(r'(\d+)\s*(min|minute)[s]?\s*(ago|before)', queryLower)
    if mins_ago_match:
        parsed["time"] = f"{mins_ago_match.group(1)}_minutes_ago"

    # -----------------------------
    # 9. TIME (X hours ago / before)
    # -----------------------------

    hrs_ago_match = re.search(r'(\d+)\s*(hr|hour)[s]?\s*(ago|before)', queryLower)
    if hrs_ago_match:
        parsed["time"] = f"{hrs_ago_match.group(1)}_hours_ago"
    return parsed


def extract_camera_id(text: str) -> int | None:
    patterns = [
        r'(camera|cam)[-\s]*(\d+)',
        r'(camera|cam)\s*id\s*(is|=|:)?\s*(\d+)',
        r'(\d+)(st|nd|th|rd)\s*(camera|cam)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.groups()[-1])
    return None
