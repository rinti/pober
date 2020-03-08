import httpx

# TEST_URL = "https://poe.ninja/challengehc/builds/char/PoEDan79/DanGuardianAbuser?i=2"

# TEST_URL = "https://poe.ninja/api/data/x/getcharacter?overview=hardcore-metamorph&account=PoEDan79&name=DanGuardianAbuser&type=exp&language=en"
TEST_URL = "https://poe.ninja/api/data/dca62e247969ac543672251a6fc66d98/getcharacter?overview=hardcore-metamorph&account=oBezz&name=Joxddd&type=exp&language=en"

def get_dps(data):
    if not len(data):
        return {"dps": 0, "skill": None}

    return list(map(lambda x: {"dps": max(x["dps"], x["dotDps"]), "skill": x["name"]}, data))[0]
    
def get_data():
    r = httpx.get(TEST_URL)
    data = r.json()

    # print(data["pathOfBuildingExport"])
    # print(data["pathOfBuildingExport"])
    # print(data["defensiveStats"]["energyShield"])
    # print(data["defensiveStats"]["life"])

    dps_data = list(filter(bool, map(lambda x: x["dps"], data["skills"])))
    dps = list(map(lambda x: get_dps(x), dps_data))
    # print(dps)

    max_dps = dps[0]["dps"] if dps else 0

    # print(max_dps)


get_data()
