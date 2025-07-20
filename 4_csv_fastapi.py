from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import csv
import io
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

EMAIL = "23f1002420@ds.study.iitm.ac.in"
EXAM_ID = "tds-2025-05-roe"

def clean_text(text: str) -> str:
    if not text:
        return ""
    return text.strip().lower()

def clean_amount(raw: str) -> float:
    if not raw:
        return 0.0
    raw = raw.strip()
    raw = raw.replace(" ", "")
 
    if ',' in raw and raw.count(',') == 1:
        raw = raw.replace('.', '')  
        raw = raw.replace(',', '.') 
    else:
 
        raw = raw.replace(',', '') 
    raw = re.sub(r"[^\d\.-]", "", raw)
    try:
        return float(raw)
    except ValueError:
        return 0.0

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    decoded = content.decode("utf-8", errors="ignore")
    reader = csv.reader(io.StringIO(decoded), delimiter=';')

    headers = next(reader, None)
    if not headers or len(headers) < 4:
        return {
            "answer": 0.0,
            "email": EMAIL,
            "exam": EXAM_ID
        }

    food_total = 0.0

    for row in reader:
        if len(row) < 4:
            continue
        row = [cell.strip() for cell in row]

        amount_str = row[2]
        category_str = row[3]

        if clean_text(category_str) == "food":
            amount = clean_amount(amount_str)
            food_total += amount

    return {
        "answer": round(food_total, 2),
        "email": EMAIL,
        "exam": EXAM_ID
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("4_csv_fastapi:app", host="0.0.0.0", port=8004, reload=True)
