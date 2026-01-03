import httpx
import asyncio

async def fetch(url: str) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        return await client.get(url)

if __name__ == "__main__":

    url = "https://httpbin.org/get"
    response = asyncio.run(fetch(url))
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
