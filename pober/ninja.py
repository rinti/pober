import httpx
import uuid

import dateutil.parser

from models import Data


def get_dps(data):
    if not len(data):
        return {"dps": 0, "skill": None}

    return list(map(lambda x: {"dps": max(x["dps"], x["dotDps"]), "skill": x["name"]}, data))[0]
    

async def create_or_update_data_for_character(character):
    urlsplit = character.url.split("/")
    urlsplit[5] = str(uuid.uuid4())
    url = "/".join(urlsplit)

    r = httpx.get(url)

    if r.status_code == 500:
        return
    else:
        print("Happy fun times", character.id)

    data = r.json()

    last_update = dateutil.parser.parse(data["updatedUtc"])

    if await Data.objects.filter(character=character, last_update=last_update).exists():
        return

    await character.update(last_update=last_update)

    dps_data = list(filter(bool, map(lambda x: x["dps"], data["skills"])))
    dps = list(map(lambda x: get_dps(x), dps_data))

    max_dps = dps[0]["dps"] if dps else 0
    max_dps_skill = dps[0]["skill"] if dps else "?"

    await Data.create_data(**{
        "character": character,
        "level": data["level"],
        "character_class": data["class"],
        "energy_shield": data["defensiveStats"]["energyShield"],
        "life": data["defensiveStats"]["life"],
        "max_dps": max_dps,
        "max_dps_skill": max_dps_skill,
        "pob_export": data["pathOfBuildingExport"],
        "data": data,
        "last_update": last_update,
    })
