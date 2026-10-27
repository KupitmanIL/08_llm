import os
import httpx
from fastapi import FastAPI, HTTPException
from loggers.logger_req import logger

FIXER_URL = "https://api.apilayer.com/fixer/convert"
API_KEY = os.environ.get('FIXER_API_KEY')

if not API_KEY:
    raise ValueError('FIXER_API_KEY environment variable not set')

async def get_exchange_rate (code_from:str ,code_to:str) -> float:
    logger.debug(f'Fetching exchange rate for {code_from} to {code_to}')
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(FIXER_URL,params={'from':code_from,'to':code_to,'amount':1}, headers={'API-KEY':API_KEY})
    except httpx.RequestError as exc:
        logger.error(f'Weather service unreachable {exc}')
        raise HTTPException(status_code=502, detail='Currency service unreachable') from exc

    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        logger.error(f'Error fetching currency exchange rate {exc}')
        raise HTTPException(status_code=502, detail=f'Error fetching currency exchange rate {exc}') from exc
    data = resp.json()
    if not data.get("success", False):
        logger.warning(f'Currency exchange rate not found for {code_from} to {code_to}')
        raise HTTPException(status_code=400,detail=f'Currency exchange rate not found for {code_from} to {code_to}')
    try:
        return data['info']['rate']
    except(KeyError, TypeError) as exc:
        logger.error(f'Unexpected currency response for {code_from} to {code_to}: {exc}')
        raise HTTPException(status_code=502, detail=f'Unexpected currency response for for {code_from} to {code_to}')