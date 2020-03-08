import datetime
import databases
import orm
import sqlalchemy

database = databases.Database("sqlite:///db.sqlite")
metadata = sqlalchemy.MetaData()

class Character(orm.Model):
    __tablename__ = "character"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    url = orm.String(max_length=200, index=True)
    last_update = orm.DateTime(allow_null=True)

    @staticmethod
    async def add_url(url):
        if not url.startswith('https://poe.ninja'):
            return

        await Character.objects.create(
            url=url,
            last_update=datetime.datetime.now()
        )

class Data(orm.Model):
    __tablename__ = "data"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    character = orm.ForeignKey(Character)

    level = orm.Integer()
    energy_shield = orm.Integer()
    life = orm.Integer()
    pob_export = orm.Text()
    max_dps = orm.Integer()
    max_dps_skill = orm.String(max_length=255)
    character_class = orm.String(max_length=255)
    data = orm.JSON()
    last_update = orm.DateTime(allow_null=True)

    @staticmethod
    async def create_data(**kwargs):
        await Data.objects.create(
            **kwargs
        )


def setup_databases():
    engine = sqlalchemy.create_engine(str(database.url))
    metadata.create_all(engine)
