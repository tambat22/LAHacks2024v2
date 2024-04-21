from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from pathlib import Path
from starlette.status import HTTP_400_BAD_REQUEST
import uvicorn
from uagents.query import query
from models import Image
from dotenv import load_dotenv
import json

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if file is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="No file uploaded")

    if file.filename == '':
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="No selected file")

    try:
        file_location = (Path(UPLOAD_FOLDER) / file.filename).resolve()
        with open(file_location, "wb") as file_data:
            file_data.write(await file.read())
        print("File saved to: ", file_location)
        try:
            response = await query(destination=os.getenv("AGENT1_ADDRESS"), message=Image(path=str(file_location)), timeout=30.0)
            data = json.loads(response.decode_payload())
            print("Agent response: ", data)
        except Exception as e:
            print("Error querying agent: ", str(e))

        return JSONResponse(content=data)
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"An error occurred: {str(e)}"})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
