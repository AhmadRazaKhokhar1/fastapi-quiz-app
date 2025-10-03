from typing import Callable, Awaitable
from fastapi import Request, Response
from helpers.logger import logger

async def track_current_request(req: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response: 
    logger_dict = {
        'path':req.url.path,
        'method': req.method
    }
    logger.info(logger_dict)
    response = await call_next(req)
    return response