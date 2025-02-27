from pydantic import BaseModel
from typing import Dict


class ParserConfig(BaseModel):
    enabled: bool


class Parsers(BaseModel):
    templator: ParserConfig


class ParserSystemConfig(BaseModel):
    enabled: bool
    parsers: Parsers
