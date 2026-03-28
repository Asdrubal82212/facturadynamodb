from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import boto3

app = FastAPI()
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("facturas")

@app.get("/", response_class=HTMLResponse)
def ver_facturas():
    response = table.scan()
    items = response.get("Items", [])
    
    filas = ""
    for item in items:
        filas += f"""
        <tr>
            <td>{item.get('factura_id','')}</td>
            <td>{item.get('archivo','')}</td>
            <td>{item.get('fecha_procesado','')}</td>
            <td><pre>{item.get('contenido','')}</pre></td>
        </tr>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Facturas DynamoDB</title>
        <style>
            body {{ font-family: Arial; padding: 30px; background: #f5f5f5; }}
            h1 {{ color: #232f3e; }}
            table {{ width: 100%; border-collapse: collapse; background: white; }}
            th {{ background: #232f3e; color: white; padding: 12px; text-align: left; }}
            td {{ padding: 10px; border-bottom: 1px solid #ddd; vertical-align: top; }}
            pre {{ margin: 0; font-size: 12px; white-space: pre-wrap; }}
            tr:hover {{ background: #f0f0f0; }}
        </style>
    </head>
    <body>
        <h1>📄 Facturas procesadas desde S3 → DynamoDB</h1>
        <p>Bucket S3: <b>facturas-imagenes-bucket</b> | Tabla DynamoDB: <b>facturas</b></p>
        <table>
            <tr>
                <th>ID Factura</th>
                <th>Archivo S3</th>
                <th>Fecha</th>
                <th>Contenido extraído</th>
            </tr>
            {filas}
        </table>
    </body>
    </html>
    """
    return html
