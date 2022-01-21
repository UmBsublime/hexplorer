from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from hexplorer.models.match_v5 import InfoDtoBase, ParticipantDtoBase


class MatchParticipantLink(SQLModel, table=True):
    matchId: Optional[int] = Field(default=None, foreign_key="info.gameId", primary_key=True)
    participantId: Optional[str] = Field(default=None, foreign_key="participant.puuid", primary_key=True)


class Info(InfoDtoBase, SQLModel, table=True):
    gameId: Optional[int] = Field(default=None, primary_key=True)
    participants: Optional[List["Participant"]] = Relationship(
        back_populates="matches", link_model=MatchParticipantLink
    )


class Participant(ParticipantDtoBase, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    matches: List[Info] = Relationship(back_populates="participants", link_model=MatchParticipantLink)
