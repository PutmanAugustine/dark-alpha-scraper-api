from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

class Sheet(BaseModel):
  id: int
  name: str
  data: dict[str, str]

app = FastAPI()

@app.get("/sheet/{sheet_id}")
async def read_item(sheet_id: int, q: Union[str, None] = None):
  return {"message": "Probably fetch a scraped data sheet", "sheet_id": sheet_id, "q": q}

@app.post("/sheet/scrape/")
async def rescrape_sheet(url: str, name: str):
  return {"data": scrape(name, url)}
