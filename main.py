import json

from fastapi import FastAPI
from starlette.responses import Response

app = FastAPI()

@app.get("/")
def root():
    return Response(content=json.dumps({"message":"Hello there!"}),status_code=200, media_type="text/html")