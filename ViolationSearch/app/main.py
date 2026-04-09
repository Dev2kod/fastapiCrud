from fastapi import FastAPI
from .api.search import router as searchRouter
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/")
def home():
    return{"msg":"server is running"}