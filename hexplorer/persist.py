from typing import TYPE_CHECKING, Any

from loguru import logger
from sqlmodel import Session, SQLModel, col, create_engine, select

from hexplorer.models.db.match import Info, Participant
from hexplorer.models.match_v5 import InfoDto

if TYPE_CHECKING:
    from sqlalchemy.future.engine import Engine


def store_matchinfo(engine: "Engine", infodto: InfoDto) -> None:
    db_match = Info.from_orm(infodto)
    db_match.participants = [Participant.from_orm(p) for p in infodto.participants]

    with Session(engine) as session:
        query = select(col(Info.gameId)).where(col(Info.gameId) == db_match.gameId)
        exists = session.exec(query).first()
        if not exists:
            logger.info(f"Storing match {db_match.platformId}_{db_match.gameId} in database")
            logger.trace(db_match)
            session.add(db_match)
            session.commit()
        else:
            logger.info(f"Match {db_match.platformId}_{db_match.gameId} already in database")
            logger.trace(exists)


def retreive_matchinfo(engine: "Engine", match: str) -> InfoDto:
    platform, match_id = match.split("_")
    with Session(engine) as session:
        query = select(Info).where(col(Info.gameId) == match_id).where(col(Info.platformId) == platform)
        match_info = session.exec(query).first()

        if match_info:
            logger.info(f"Found match {match} in database")
            return InfoDto.from_orm(match_info)

        else:
            logger.warning(f"Match {match} not found in database")
            return None


def create_db_and_tables(engine: "Engine"):
    SQLModel.metadata.create_all(engine)


class PersistanceManager:
    obj_mapping = {
        InfoDto: {"store": store_matchinfo, "retreive": retreive_matchinfo},
    }

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        SQLModel.metadata.create_all(self.engine)

    def store(self, obj: Any) -> None:
        obj_type = type(obj)
        funcs = self.obj_mapping.get(obj_type, None)
        if funcs:
            return funcs["store"](self.engine, obj)

    def retreive(self, identifier: Any, obj_type: Any) -> Any:
        funcs = self.obj_mapping.get(obj_type, None)
        if funcs:
            return funcs["retreive"](self.engine, identifier)
