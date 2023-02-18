from typing import Optional

from sqlmodel import Field, SQLModel, create_engine, Session, select, col, Relationship
from hexplorer import RiotApiDispatch
from hexplorer.config import SETTINGS
from hexplorer.constants import Region
from hexplorer.models.summoner_v4 import SummonerDTO


class DBSummonerDTO(SummonerDTO, SQLModel, table=True):
    id: str = Field(primary_key=True, description="Encrypted summoner ID. Max length 63 characters.")
    name: str = Field(..., index=True, description="Summoner name.")


class Toto(SQLModel, table=True):

    id: str = Field(primary_key=True, default=None)
#    user: DBSummonerDTO = Relationship(sa_relationship_kwargs=dict(foreign_keys="[DBSummonerDTO.id]"))


api = RiotApiDispatch(SETTINGS.api_key)
me = api.lol.summoner.by_name(Region.NA1, 'SillyPlays')
sql_me = DBSummonerDTO(**me.dict())
#print(sql_me)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)
#SQLModel.co
SQLModel.metadata.create_all(engine)

#session = Session(engine)

with Session(engine) as session:
    if not session.exec(select(DBSummonerDTO).where(col(DBSummonerDTO.name) == 'SillyPlays')).first():
        session.add(sql_me)
        session.commit()
#me_db = 
#if not me_db:
#    session.add(sql_me)
#    session.commit()
#else:
#    print("Exists:", me_db)
#print(result.all())
#for res in result:
#print(result.one())
#if not result.all():
#    session.add(sql_me, _warn=False)
#else:
#    print(result.all())

print('hello')
