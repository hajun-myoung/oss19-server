from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Status": "200 OK", "Purpose": "OS19", "Author": "Chanwoo"}

@app.get("/ingredients/:page")
def get_ingredients():
    return False
