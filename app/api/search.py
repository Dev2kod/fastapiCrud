from fastapi import APIRouter
from app.models.schema import SearchRequest
from app.core.queryParser import parseQuery
from app.services.queryService import violationFiltering
from app.core.dataLoader import get_violations
from app.services.timestampCalculator import calculate_time_range

router = APIRouter()



#parsed query format:
# {parsed = {
    #     "camera_id": None,
    #     "severity": None,
    #     "violation_type": None,
    #     "site": None,
    #     "time": None,
    #     "sort": None,
    #     "text": query
    # }
@router.post("/search")
def search(request: SearchRequest):
    fileteredquery = {
        "camera_id": None,
        "severity": None,
        "violation_type": None,
        "site": None,
        "sort": None,
        "Start_DateTime": None,
        "End_DateTime": None,
    }
    data = get_violations()
    parsedQuery = parseQuery(request.query)
    results = violationFiltering(parsedQuery,data)
    print(f"Parsed Query: {parsedQuery}")
    
    return {
        "parsed_query": parsedQuery,
        "results": results
    }
    
    
@router.post("/filterData")
def filter_data(request: SearchRequest):
    
    data = get_violations()
    parsedQuery = parseQuery(request.query)
    convertedTime = None
    if parsedQuery.get("time"):
        convertedTime = calculate_time_range(parsedQuery.get("time"))
    
    if convertedTime:
        parsedQuery["Start_DateTime"] = convertedTime["start_time"]
        parsedQuery["End_DateTime"] = convertedTime["end_time"]

    filter = {
        "Camera_ID": parsedQuery.get("camera_id"),
        "Severity": parsedQuery.get("severity"),
        "ViolationType": parsedQuery.get("violation_type"),
        "Site": parsedQuery.get("site"),
        "Start_DateTime": convertedTime["start_time"] if convertedTime else None,
        "End_DateTime": convertedTime["end_time"] if convertedTime else None
    }    
    
    data = get_violations()
    
    
    results = violationFiltering(filter, data)
    print(f"Filter count: {len(results)}")

    return {
        "parsed_query": parsedQuery,
        "filter": filter,
        "results": results
    }
    
    
    
# @router.post("/testTime")
# def test_time(request: SearchRequest):
#     parsedQuery = parseQuery(request.query)
#     time_str = parsedQuery.get("time")
#     time_range = calculate_time_range(time_str)
#     print(f"Parsed Time: {time_str}, Time Range: {time_range}")
#     return {
#         "start_time": time_range["start_time"],
#         "end_time": time_range["end_time"]
#     }
    
#async route
@router.post("/async")
async def test_time_async(request: SearchRequest):
    parsedQuery = parseQuery(request.query)
    time_str = parsedQuery.get("time")
    time_range = calculate_time_range(time_str)
    print(f"Parsed Time: {time_str}, Time Range: {time_range}")
    return {
        "start_time": time_range["start_time"],
        "end_time": time_range["end_time"]
    }


#---------------------------------------------------API LLM---------------------------------------------------------------


from pydantic import BaseModel
import requests
from app.api.bypassSsl import bypassSsl

# Bypass SSL verification

HF_API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-8B-Instruct"
HF_API_TOKEN = "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"

headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

class PromptRequest(BaseModel):
    prompt: str

@router.post("/generate")
async def generate_text(request: PromptRequest):
    bypassSsl()
    payload = {"inputs": request.prompt}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    return response.json()
