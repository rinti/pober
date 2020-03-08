from asyncio import sleep, ensure_future

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.templating import Jinja2Templates
from starlette.background import BackgroundTask

from models import setup_databases, Character, Data
from ninja import create_or_update_data_for_character

SLEEP_TIME = 60 * 60

templates = Jinja2Templates(directory='templates')


async def check_for_updates():
    for character in await Character.objects.all():
        await create_or_update_data_for_character(character)

    await sleep(SLEEP_TIME)
    await check_for_updates()


async def setup():
    setup_databases()
    ensure_future(check_for_updates())


async def profile(request):
    id = request.path_params['character_id']

    character = await Character.objects.get(id=id)

    context = {
        "request": request,
        "data": await Data.objects.filter(character=character).all(),
    }

    return templates.TemplateResponse("profile.html", context)

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
    Route("/", endpoint=homepage, methods=["GET", "POST"]),
    Route("/{character_id:int}", endpoint=profile)
]

app = Starlette(debug=True, routes=routes, on_startup=[setup])
