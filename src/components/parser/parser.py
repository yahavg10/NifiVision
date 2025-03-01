from typing import List, Dict

from src.components.parser.base import AbstractParser
from src.utils import Service


@Service
class Parser:
    def __init__(self):
        self.parsers: Dict[str, AbstractParser] = {}

    def register_parsers(self, parsers: List[AbstractParser]):
        for parser in parsers:
            self.parsers[parser.__name__] = parser

    def parse(self, raw_data, parsers_names: List = None):
        parsers_to_use = self.parsers.values() if parsers_names is None\
            else (self.parsers[name] for name in parsers_names if name in self.parsers)

        for parser in parsers_to_use:
            raw_data = parser.parse(raw_data)
        return raw_data

