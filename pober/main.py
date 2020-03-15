from urllib.parse import urlparse, parse_qs
from asyncio import sleep, ensure_future

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.templating import Jinja2Templates
from starlette.background import BackgroundTask

from models import setup_databases, Character, Data
from ninja import create_or_update_data_for_character

SLEEP_TIME = 60 * 30

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

    characters = []
    chars = await Character.objects.all()

    for char in chars:
        data = await Data.objects.filter(character=char).all()
        url = urlparse(char.url)
        qs = parse_qs(url.query)
        characters.append({
            "id": char.id,
            "updated": data[-1].last_update,
            "account": qs["account"][0],
            "name": qs["name"][0],
            "level": data[-1].level,
        })


    context = {
        "request": request,
        "characters": characters,
    }
    return templates.TemplateResponse("index.html", context)

routes = [
    Route("/", endpoint=homepage, methods=["GET", "POST"]),
    Route("/{character_id:int}", endpoint=profile)
]

app = Starlette(debug=True, routes=routes, on_startup=[setup])
