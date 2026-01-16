import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# 1. Carichiamo le variabili dal file .env
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

app = FastAPI(title="IoT-Workforce-Ecosystem API")

class Attendance(BaseModel):
    operator_id: str
    action: str
    timestamp: str
    battery_voltage: float

@app.get("/")
def home():
    return {"message": "Backend is running!"}

@app.post("/log_attendance")
async def log_attendance(record: Attendance):
    # Controlliamo che le chiavi siano state caricate correttamente
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise HTTPException(status_code=500, detail="Missing Supabase credentials in .env")

    url = f"{SUPABASE_URL}/rest/v1/presenze"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    payload = {
        "operator": record.operator_id,
        "action": record.action,
        "timestamp": record.timestamp,
        "voltage": record.battery_voltage
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            # Nota: Supabase restituisce 201 se creato con successo
            if response.status_code in [200, 201]:
                return {"status": "success", "message": "Saved to Cloud"}
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")