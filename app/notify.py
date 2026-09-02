from __future__ import annotations

import logging
import secrets
from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from app.settings import Settings

logger = logging.getLogger(__name__)


async def send_vk(token: str, peer_id: str, text: str) -> bool:
    if not token or not peer_id:
        return False
    payload = {
        "access_token": token,
        "v": "5.199",
        "peer_id": peer_id,
        "random_id": secrets.randbelow(2_147_483_647),
        "message": text,
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post("https://api.vk.com/method/messages.send", data=payload)
    body = response.json()
    if response.status_code != 200 or "error" in body:
        logger.warning("VK notify failed: %s", body.get("error", response.status_code))
        return False
    return "response" in body


async def send_max(token: str, user_id: str, chat_id: str, text: str) -> bool:
    if not token or (not user_id and not chat_id):
        return False
    params: dict[str, str] = {}
    if chat_id:
        params["chat_id"] = chat_id
    else:
        params["user_id"] = user_id
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            "https://platform-api2.max.ru/messages",
            params=params,
            headers={
                "Authorization": token,
                "Content-Type": "application/json",
            },
            json={"text": text},
        )
    if response.status_code != 200:
        logger.warning("MAX notify failed: %s %s", response.status_code, response.text[:300])
        return False
    return True


async def notify_lead(settings: Settings, text: str) -> tuple[bool, bool]:
    vk_ok = await send_vk(settings.vk_access_token, settings.vk_peer_id, text)
    max_ok = await send_max(
        settings.max_bot_token,
        settings.max_user_id,
        settings.max_chat_id,
        text,
    )
    return vk_ok, max_ok
