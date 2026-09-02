from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.db import init_db, insert_lead
from app.notify import notify_lead
from app.settings import settings


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    await init_db(settings.database_path)
    yield


app = FastAPI(title=settings.site_name, lifespan=lifespan)
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


def _ctx(request: Request, **extra: object) -> dict[str, object]:
    return {
        "request": request,
        "site_name": settings.site_name,
        "phone": settings.site_phone,
        "phone_tel": settings.site_phone_tel,
        "city": settings.site_city,
        **extra,
    }


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html", _ctx(request))


@app.get("/spasibo", response_class=HTMLResponse)
async def thanks(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "thanks.html", _ctx(request))


@app.post("/zayavka")
async def create_lead(
    name: str = Form(default=""),
    phone: str = Form(),
    material: str = Form(default="щебень"),
    volume: str = Form(default="одна машина"),
    address: str = Form(default=""),
    when_needed: str = Form(default="как можно скорее"),
    comment: str = Form(default=""),
) -> RedirectResponse:
    phone_clean = phone.strip()
    if not phone_clean:
        return RedirectResponse("/#zayavka", status_code=303)

    name_clean = name.strip() or "без имени"
    material_clean = material.strip() or "щебень"
    volume_clean = volume.strip() or "одна машина"
    address_clean = address.strip() or "не указан"
    when_clean = when_needed.strip() or "как можно скорее"
    comment_clean = comment.strip()

    text = "\n".join(
        [
            "Новая заявка с сайта",
            f"Имя: {name_clean}",
            f"Телефон: {phone_clean}",
            f"Материал: {material_clean}",
            f"Объём: {volume_clean}",
            f"Адрес: {address_clean}",
            f"Когда: {when_clean}",
            f"Комментарий: {comment_clean or '—'}",
        ]
    )
    vk_ok, max_ok = await notify_lead(settings, text)
    await insert_lead(
        settings.database_path,
        name=name_clean,
        phone=phone_clean,
        material=material_clean,
        volume=volume_clean,
        address=address_clean,
        when_needed=when_clean,
        comment=comment_clean,
        vk_ok=vk_ok,
        max_ok=max_ok,
    )
    return RedirectResponse("/spasibo", status_code=303)
