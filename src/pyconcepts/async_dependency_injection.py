# Use this pattern to manage the lifecycle of long-running asynchronous tasks in your application.

from typing import AsyncIterator
from contextlib import asynccontextmanager

import asyncio

@asynccontextmanager
async def lifespan() -> AsyncIterator[None]:
    print("startup")
    yield
    print("shutdown")

async def main():
    async with lifespan():
        print("Application is running...")

if __name__ == "__main__":

    asyncio.run(main())