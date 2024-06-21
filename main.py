from typing import Union, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import os
import uvicorn

app = FastAPI()

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("firebase_credential.json")
firebase_admin.initialize_app(cred)


origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Status": "200 OK", "Purpose": "OS19", "Author": "Chanwoo"}

@app.post("/getrecipe")
async def getRecipeByGPT():

    return True

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Default to 8000 if PORT not set
    uvicorn.run(app, host="0.0.0.0", port=port)