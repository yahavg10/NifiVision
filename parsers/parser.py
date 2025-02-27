from typing import List, Dict

from parsers.base import AbstractParser


class Parser:
    def __init__(self):
        self.parsers: Dict[str, AbstractParser] = {}

    def register_parser(self, parser: AbstractParser):
        self.parsers[parser.__class__.__name__] = parser

    def parse(self, raw_data, parsers_names: List = None):
        parsers_to_use = self.parsers.values() if parsers_names is None\
            else (self.parsers[name] for name in parsers_names if name in self.parsers)

        for parser in parsers_to_use:
            raw_data = parser.parse(raw_data)
        return raw_data

