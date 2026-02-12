import json
from io import StringIO

import httpx
import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

"""
async def fetch(url: str) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        return await client.get(url)
    
async def fetch_stock_data(symbol: str) -> httpx.Response:
        #url = f"https://stooq.com/q/l/?s={symbol.lower()}&f=sd2t2ohlcv&h&e=csv"
        url = f"https://stooq.com/q/d/l/?s={symbol.lower()}.us&i=d"
        return await fetch(url)

async def main():
    url = "https://httpbin.org/get"
    response = await fetch(url)
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    # Get Top 5 oldest stocks data from stooq.com
    stock_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    
    tasks = [fetch_stock_data(symbol) for symbol in stock_symbols]
    responses = await asyncio.gather(*tasks)
    for response in responses:
        print(response.text)

if __name__ == "__main__":
    asyncio.run(main())
"""

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/stock/{symbol}")
async def get_stock_data(symbol: str):
    url = f"https://stooq.com/q/d/l/?s={symbol.lower()}.us&i=d"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            # format the response from csv to json
            response = pd.read_csv(StringIO(response.text))
            json_response = response.to_json(orient="records")
            return JSONResponse(content={"data": json.loads(json_response)})
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=str(e)) from e


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
