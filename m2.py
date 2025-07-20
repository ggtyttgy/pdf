from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from typing import Dict
import io

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)) -> Dict[str, int]:
    contents = await file.read()
    total_sum = 0

    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if not row or row[0] == "Product":
                        continue
                    if row[0].strip().lower() == "widget":
                        try:
                            total_sum += int(row[3])
                        except (ValueError, IndexError):
                            pass

    return {"sum": total_sum}
