from typing import Union
from fastapi import FastAPI

import csv

app = FastAPI()


@app.get("/")
def read_root():
    return {"Status": "200 OK", "Purpose": "OS19", "Author": "Chanwoo"}

@app.get("/ingredients/{page_number}")
def get_ingredients(page_number: int):
    ingredients = []

    ## Mocked up Ingredients Database
    # TODO: Need to migrate to real database
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

    slicedData = ingredients[page_number: page_number+10]

    return {"ingredients": slicedData}
