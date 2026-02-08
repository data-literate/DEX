# Use this pattern to manage the lifecycle of long-running asynchronous
# tasks in your application.

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager


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
