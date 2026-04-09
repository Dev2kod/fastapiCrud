from pydantic import BaseModel

class SearchRequest(BaseModel):
    query:str
    
    
    
# filter = {
#         "Camera_ID": parsedQuery.get("camera_id"),
#         "Severity": parsedQuery.get("severity"),
#         "ViolationType": parsedQuery.get("violation_type"),
#         "Site": parsedQuery.get("site"),
#         "Start_DateTime": convertedTime["start_time"] if convertedTime else None,
#         "End_DateTime": convertedTime["end_time"] if convertedTime else None
#     }    
class FilterRequest(BaseModel):
    camera_id: int = None
    severity: str = None
    violation_type: str = None
    site: str = None
    Start_DateTime: str = None
    End_DateTime: str = None
    
    