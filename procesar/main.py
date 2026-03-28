from fastapi import FastAPI
import boto3
import uuid
import pdfplumber
import tempfile
import os

app = FastAPI()
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("facturas")
s3 = boto3.client("s3", region_name="us-east-1")
BUCKET = "facturas-imagenes-bucket"

@app.post("/procesar/{nombre_archivo}")
def procesar_factura(nombre_archivo: str):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp_path = tmp.name

    s3.download_file(BUCKET, nombre_archivo, tmp_path)

    texto = ""
    with pdfplumber.open(tmp_path) as pdf:
        for page in pdf.pages:
            texto += page.extract_text(x_tolerance=3, y_tolerance=3) or ""
    os.unlink(tmp_path)

    texto = texto.encode('latin-1', errors='ignore').decode('utf-8', errors='ignore')

    factura_id = str(uuid.uuid4())
    item = {
        "factura_id": factura_id,
        "archivo": nombre_archivo,
        "contenido": texto[:1000],
        "fecha_procesado": "2026-03-28"
    }
    table.put_item(Item=item)
    return {"mensaje": "Factura procesada", "factura": item}
