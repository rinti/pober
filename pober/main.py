from asyncio import sleep, ensure_future

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.templating import Jinja2Templates
from models import setup_databases, Character

SLEEP_TIME = 600

templates = Jinja2Templates(directory='templates')


async def check_for_updates():

    await sleep(SLEEP_TIME)
    await check_for_updates()


async def setup():
    setup_databases()
    # await Character.objects.create(url="https://poe.ninja/challengehc/builds/char/oBezz/Joxddd?i=0")
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
