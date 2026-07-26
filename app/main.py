from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from app.core.ai_engine import run_unified_scanner

app = FastAPI(
    title="ZeroTrust One Platform API",
    version="3.0.0",
    description="Unified Zero Trust Cyber Defense Platform API"
)

# Enable CORS for browser extensions and external web dashboards
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    scan_type: str
    content: str

@app.get("/")
def health_check():
    return {
        "status": "online",
        "platform": "ZeroTrust One",
        "version": "3.0.0",
        "engine": "Unified Multi-LLM Defense Active"
    }

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(content=b"", media_type="image/x-icon")

@app.post("/api/v1/scan")
async def scan_payload(payload: ScanRequest):
    if not payload.content.strip():
        raise HTTPException(status_code=400, detail="Scan content cannot be empty.")
    
    result = await run_unified_scanner(payload.content, payload.scan_type)
    return {
        "status": "success",
        "input_type": payload.scan_type,
        "analysis": result
    }
