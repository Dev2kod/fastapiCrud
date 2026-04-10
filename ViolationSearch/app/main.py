from fastapi import FastAPI
from .api.search import router as searchRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text

Database_URL = "sqlite:///D:\\safety-monitor\\ViolationSearch\\app\\violations.db"
engine = create_engine(Database_URL, echo=True)
    

# from app.core.llmParser import testLlm
app = FastAPI()

app.add_middleware(
    CORSMiddleware, #imported above
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(searchRouter)

@app.get("/violations")
def get_violations():
    
    query = "SELECT v.Violation_ID AS id,v.TimeStamp,v.Camera_ID,v.Severity,GROUP_CONCAT(d.ViolationType_ID) AS violation_type_ids FROM Violations v JOIN ViolationDetails d ON v.Violation_ID = d.Violation_ID GROUP BY v.Violation_ID, v.TimeStamp, v.Camera_ID, v.Severity;"

    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            data = [dict(row._mapping) for row in result]
        return {"data": data}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def home():
    return{"msg":"server is running"}