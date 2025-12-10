from typing import Annotated, AsyncGenerator

import httpx
from fastapi import Depends


async def get_api_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient() as client:
        yield client


api_client_dep = Annotated[httpx.AsyncClient, Depends(get_api_client)]
