from pydantic import BaseModel
from typing import Dict


class ParserConfig(BaseModel):
    enabled: bool


class Parsers(BaseModel):
    templator: ParserConfig


class ParserSystemConfig(BaseModel):
    enabled: bool
    parsers: Parsers


from pydantic import BaseModel, HttpUrl, Field
from typing import Optional


class TLSConfig(BaseModel):
    insecure_skip_verify: bool


class PrometheusConfig(BaseModel):
    url: HttpUrl
    query_timeout: str = Field(pattern=r'^\d+[smhd]$')  # Example: 30s, 1m, 1h
    query: str
    tls_config: Optional[TLSConfig]


class DataSourceConfig(BaseModel):
    prometheus: PrometheusConfig
