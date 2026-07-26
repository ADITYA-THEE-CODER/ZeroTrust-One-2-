from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.core.ai_engine import run_unified_scanner

app = FastAPI(
    title="ZeroTrust One Defense Platform API",
    version="3.0.0",
    description="Unified Cyber Defense API engine with server-side Multi-LLM consensus."
)

# CORS setup to allow access from local tests, web apps, and Chrome Extensions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    scan_type: str  # e.g., "email", "url", "text", "file_metadata"
    content: str

@app.get("/")
def health_check():
    return {
        "status": "online",
        "platform": "ZeroTrust One",
        "version": "3.0.0",
        "engine": "Unified Multi-LLM Defense Active"
    }

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
