from app.models.schema import FilterRequest

def violationFiltering(filter: FilterRequest, data):
    results = data

    if filter.get("Camera_ID"):
        results = [r for r in results if r["Camera_ID"] == filter["Camera_ID"]]
    if filter.get("Severity"):
        results = [r for r in results if r["Severity"].lower() == filter["Severity"].lower()]
    if filter.get("ViolationType"):
        results = [r for r in results if r["ViolationType"].lower() == filter["ViolationType"].lower()]
    if filter.get("Site"):
        results = [r for r in results if r["Site"].lower() == filter["Site"].lower()]
    if filter.get("Start_DateTime") and filter.get("End_DateTime"):
        results = [r for r in results if filter["Start_DateTime"] <= r["Timestamp"] <= filter["End_DateTime"]]
        
    return results

def generateSQLQuery(filter: FilterRequest):
    sql_query = "SELECT * FROM violations WHERE 1=1"
    if filter.get("Camera_ID"):
        sql_query += f" AND Camera_ID = {filter['Camera_ID']}"
    if filter.get("Severity"):
        sql_query += f" AND Severity = '{filter['Severity']}'"
    if filter.get("ViolationType"):
        sql_query += f" AND ViolationType = '{filter['ViolationType']}'"
    if filter.get("Site"):
        sql_query += f" AND Site = '{filter['Site']}'"
    if filter.get("Start_DateTime") and filter.get("End_DateTime"):
        sql_query += f" AND Timestamp BETWEEN '{filter['Start_DateTime']}' AND '{filter['End_DateTime']}'"
    return sql_query