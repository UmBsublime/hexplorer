from __future__ import annotations

from typing import List

from pydantic import BaseModel


class RuneDTO(BaseModel):
    id: int
    key: str
    icon: str
    name: str
    shortDesc: str
    longDesc: str


class RuneSelectionDTO(BaseModel):
    runes: List[RuneDTO]


class RuneStyleDTO(BaseModel):
    id: int
    key: str
    icon: str
    name: str
    slots: List[RuneSelectionDTO]
