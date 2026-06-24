from fastapi import APIRouter
from typing import Dict
import os
import json
from datetime import datetime

router = APIRouter()

@router.get("/")
async def get_metrics() -> Dict:
    """Tra ve cac metric su dung co ban tu file log JSONL"""
    log_file = "logs/structured_requests.jsonl"
    if not os.path.exists(log_file):
        return {"status": "no_data", "total_requests": 0}
        
    total_requests = 0
    intent_counts = {}
    total_duration = 0
    
    # Phan tich 1000 dong cuoi cung de lay metric tranh loi memory
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()[-1000:]
            for line in lines:
                try:
                    data = json.loads(line)
                    total_requests += 1
                    
                    intent = data.get("intent", "unknown")
                    intent_counts[intent] = intent_counts.get(intent, 0) + 1
                    
                    total_duration += data.get("duration_ms", 0)
                except:
                    continue
                    
        return {
            "status": "success",
            "analyzed_requests": total_requests,
            "avg_duration_ms": round(total_duration / total_requests if total_requests > 0 else 0, 2),
            "intent_distribution": intent_counts
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
