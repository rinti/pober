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

def setup_databases():
    engine = sqlalchemy.create_engine(str(database.url))
    metadata.create_all(engine)
