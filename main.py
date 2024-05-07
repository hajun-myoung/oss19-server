from typing import Union, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import csv

app = FastAPI()

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

@app.get("/ingredients")
def get_ingredients(page: Optional[int] = None, query: Optional[str] = None, term: Optional[int] = 10):
    ingredients = []

    ## Mocked up Ingredients Database
    # TODO: Need to migrate to real database
    filename = "ingredients.csv"
    with open(filename, "r") as file:
        # FIXME: Below code is using n+1 antipattern
        # When migrating this to the real databse,
        # fix it to the method that not using the antipattern
        reader = csv.reader(file)
        for row in reader:
            for item in row:
                ingredients.append(item)
        file.close()

    result = []
    if query is not None:
        for ingredient in ingredients:
            if query in ingredient:
                result.append(ingredient)
    else:
        result = ingredients[page * term: page * term + term]

    if len(result) == 0:
        raise HTTPException(status_code=404, detail="Ingredients Not Found")
    else:
        # return {
        #     "status": "200 OK",
        #     "result": result
        # }
        return {"result": result}
    
# @app.post("/")

# TODO: Create new ingredients
# Recommend to make it after connect to the real databse
# Cuz, creating to mockup DB(the csv file) is useless

# TODO: Update an ingredient

# TODO: Delete an ingredient

# @app.get("/ingredients")
