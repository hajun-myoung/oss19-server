from typing import Union, Optional
from fastapi import FastAPI

import csv

app = FastAPI()


@app.get("/")
def read_root():
    return {"Status": "200 OK", "Purpose": "OS19", "Author": "Chanwoo"}

@app.get("/ingredients")
def get_ingredients(page: Optional[int] = None, query: Optional[str] = None, term: Optional[int] = 10):
    ingredients = []

    # ## Mocked up Ingredients Database
    # # TODO: Need to migrate to real database
    filename = "ingredients.csv"
    with open(filename, "r") as file:
        # FIXME: Below code is using n+1 antipattern
        # When you migrate this to the real databse,
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
        return FileNotFoundError("No Ingredients Has Been Queried")
    else:
        return {
            "status": "200 OK",
            "result": result
        }

# TODO: Create new ingredients

# @app.get("/ingredients")