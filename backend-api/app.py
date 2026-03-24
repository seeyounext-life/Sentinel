from fastapi import FastAPI, HTTPException
import hashlib
import json

app = FastAPI(title="Sentinel Backend API")

def verify_data_integrity(payload: dict, received_hash: str):
    """ตรวจสอบว่าข้อมูลถูกดัดแปลงหรือไม่"""
    payload_string = json.dumps(payload, sort_keys=True)
    calculated_hash = hashlib.sha256(payload_string.encode()).hexdigest()
    return calculated_hash == received_hash

@app.post("/api/v1/upload-evidence")
async def upload_evidence(data: dict):
    payload = data.get("payload")
    received_hash = data.get("hash_signature")
    
    if not payload or not received_hash:
        raise HTTPException(status_code=400, detail="Invalid data format")
        
    # 1. ตรวจสอบความสมบูรณ์ของข้อมูล (Data Integrity Check)
    is_valid = verify_data_integrity(payload, received_hash)
    
    if not is_valid:
        # ถ้า Hash ไม่ตรง แปลว่ามีคนแฮ็กแก้ข้อมูลระหว่างทาง!
        raise HTTPException(status_code=403, detail="SECURITY ALERT: Data Integrity Compromised!")
        
    # 2. ถ้าข้อมูลปลอดภัย บันทึกลง Database (จำลอง)
    print(f"Verified Evidence for {payload['patient_id']} saved to database.")
    
    return {
        "status": "success",
        "message": "Evidence verified and secured.",
        "triage_color": payload["ai_analysis"]["severity"]
    }
