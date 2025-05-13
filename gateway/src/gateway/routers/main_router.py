from exceptions import NotFoundException, GatewayTimeoutException
from globals import SERVICE_NOT_RESPONDING_TIMEOUT
from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse
from log.loggers import MAIN_ROUTER_LOGGER
from urllib.parse import urljoin
from multidict import MultiDict
import aiohttp
import asyncio

main_router = APIRouter()

SERVICES_URLS = {
    "auth-service": "http://auth-service:8081",
    "comment-service": "http://comment-service:8082",
    "user-service": "http://user-service:8084",
    "video-service": "http://video-service:8085"
}
STATIC_NGINX_URL = "http://static-nginx"


@main_router.api_route("/api/{service}/{path:path}", methods=["GET", "POST", "PUTCH", "DELETE", "PUT", "UPDATE", "OPTION"])
async def proxy_api(service: str, path: str, req: Request, resp: Response):
    if service not in SERVICES_URLS:
        raise NotFoundException("Cannot find such service!")

    target_url = urljoin(SERVICES_URLS[service], path)

    MAIN_ROUTER_LOGGER.debug(f"Routing {target_url}")

    async with aiohttp.ClientSession() as session:
        session: aiohttp.ClientSession

        data = await req.body()
        headers = dict(req.headers)

        try:
            async with session.request(
                method=req.method,
                url=target_url,
                headers=headers,
                data=data,
                params=req.query_params,
                timeout=SERVICE_NOT_RESPONDING_TIMEOUT
            ) as response:
                filtered_headers = MultiDict(response.headers)
                filtered_headers.pop("date", None)
                filtered_headers.pop("server", None)

                return Response(
                    content=(await response.read()),
                    status_code=response.status,
                    headers=filtered_headers
                )
        except asyncio.TimeoutError:
            raise GatewayTimeoutException("Service is not responding")

    
@main_router.get("/static/{path:path}")
async def proxy_static(request: Request, path: str):
    return f"{path}"

    target_url = urljoin(STATIC_NGINX_URL, path)

    async with aiohttp.ClientSession() as session:
        session: aiohttp.ClientSession

        async with session.get(target_url) as response:
            return StreamingResponse(
                content=response.content,
                status_code=response.status,
                headers=dict(response.headers),
            )
