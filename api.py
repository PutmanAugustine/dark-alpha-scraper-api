from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from scraper import scrape

class Sheet(BaseModel):
  id: int
  name: str
  data: dict[str, str]

app = FastAPI()

@app.get("/scrape/")
async def rescrape_sheet(url: str, name: str):
  return {"data": await scrape(name, url)}
