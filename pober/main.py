from asyncio import sleep, ensure_future

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.templating import Jinja2Templates
from starlette.background import BackgroundTask

from models import setup_databases, Character
from ninja import create_or_update_data_for_character

SLEEP_TIME = 10

templates = Jinja2Templates(directory='templates')


async def check_for_updates():
    for character in await Character.objects.all():
        await create_or_update_data_for_character(character)

    await sleep(SLEEP_TIME)
    await check_for_updates()


async def setup():
    setup_databases()
    ensure_future(check_for_updates())


async def homepage(request):
    if request.method == "POST":
        data = await request.form()
        await Character.add_url(data["url"])

    context = {
        "request": request,
        "characters": await Character.objects.all(),
    }
    return templates.TemplateResponse("index.html", context)

routes = [
    Route("/", endpoint=homepage, methods=["GET", "POST"])
]

app = Starlette(debug=True, routes=routes, on_startup=[setup])
