from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger("fbreaper.api")
app = FastAPI()

status_info = {"status": "ok", "service": "FBReaper Microservice"}

@app.get("/status")
def status():
    return JSONResponse(content=status_info)

# Optionally, add endpoints to trigger scraping or fetch last results
