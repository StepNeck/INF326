from fastapi import FastAPI

import json

app = FastAPI()

@app.get("/sismos/{earthquake_id}")
def read_item(earthquake_id: str):
    with open("earthquakes.json") as f:
        earthquakes = json.load(f)
    
    for earthquake in earthquakes:
        if earthquake["id"] == earthquake_id:
            return earthquake
