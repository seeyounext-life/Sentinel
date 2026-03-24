import hashlib
import json
import time

def anonymize_patient_data(patient_name):
    """ฟังก์ชันจำลองการแปลงชื่อคนไข้เป็นรหัส (Tokenization)"""
    # ในของจริงอาจจะใช้เทคนิคซับซ้อนกว่านี้
    token = hashlib.md5(patient_name.encode()).hexdigest()[:8]
    return f"PATIENT-{token.upper()}"

def run_ai_inference(image_data):
    """จำลองการให้ AI (เช่น TFLite) วิเคราะห์ภาพ"""
    # สมมติว่า AI วิเคราะห์เสร็จแล้วได้ผลลัพธ์
    return {
        "condition": "Tonsillitis",
        "confidence": 0.92,
        "severity": "Green"
    }

def generate_evidence_pack(patient_name, image_data):
    """สร้างพยานวัตถุดิจิทัลที่แก้ไขไม่ได้"""
    patient_id = anonymize_patient_data(patient_name)
    ai_result = run_ai_inference(image_data)
    
    # สร้าง Payload
    payload = {
        "patient_id": patient_id,
        "timestamp": int(time.time()),
        "ai_analysis": ai_result,
        "image_status": "attached"
    }
    
    # ทำ Digital Fingerprint (SHA-256) เพื่อป้องกันการดัดแปลง
    payload_string = json.dumps(payload, sort_keys=True)
    digital_signature = hashlib.sha256(payload_string.encode()).hexdigest()
    
    return {
        "payload": payload,
        "hash_signature": digital_signature
    }

# --- ทดสอบการทำงาน (Demo) ---
if __name__ == "__main__":
    print("[-] Sentinel Edge Node Started...")
    evidence = generate_evidence_pack("Somchai Jaidee", "raw_image_bytes_here")
    
    print("\n[+] Evidence Pack Generated (Ready to send to Cloud):")
    print(json.dumps(evidence, indent=2))
