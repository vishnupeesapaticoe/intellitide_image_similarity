from fastapi import FastAPI
from request_model import ImageRequest
import uvicorn
from middleware import add_process_time_header
from similarity_service import get_image_report,get_image_report_base64
import traceback
from rich.console import Console
console = Console()
app = FastAPI()
@app.post("/predict")
async def predict(request : ImageRequest):
    try:
        return get_image_report(request.source_url,request.target_url)
    except Exception as e:
        console.log(request)
        return {'exception':str(e)}



@app.post("/predict_base64")
async def predict(request : ImageRequest):
    try:
        return get_image_report_base64(request.source_url,request.target_url)
    except Exception as e:
        print(e)
        console.log(request)
        return {'exception':str(e)}

app.add_middleware(add_process_time_header)


if __name__ == "__main__":
    uvicorn.run("app:app", reload =False, host="0.0.0.0",port=8008,workers=8)
