from fastapi import FastAPI, HTTPException
import requests_cache
import requests
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Champion Prices API",
    description="Returns champion price information by id/key from Meraki Data",
    version="1.0.0"
)

requests_cache.install_cache(expire_after=360)

class Skin(BaseModel):
    name: str
    id: int
    cost: int
    sale: int

class Price(BaseModel):
    blueEssence: int
    rp: int
    saleRp: int

class Champion(BaseModel):
    price: Price
    skins: List[Skin]


@app.get("/champion/id/{id}", response_model=Champion)
def champion_by_id(id):
    cdragon = requests.get('https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-summary.json').json()
    try:
        [champ] = [champ['alias'] for champ in cdragon if champ['id'] == int(id)]
    except ValueError:
        raise HTTPException(status_code=404, detail="Invalid Champion ID")
    return champion_by_key(champ)

@app.get("/champion/key/{key}", response_model=Champion)
def champion_by_key(key):
    champs = requests.get('http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions.json').json()
    if key not in champs:
        raise HTTPException(status_code=404, detail="Invalid Champion Key")
    return {
        "price": champs[key]['price'],
        "skins": [{
            'name': skin['name'],
            'id': skin['id'],
            'cost': skin['cost'],
            'sale': skin['sale']
        } for skin in champs[key]['skins']]
    }