from typing import Optional, Dict

from pydantic import BaseModel, HttpUrl, Field


class ParserConfig(BaseModel):
    enabled: bool

class ParserSystemConfig(BaseModel):
    enabled: bool
    path: str
    parsers: Optional[Dict[str, ParserConfig]]

class TLSConfig(BaseModel):
    insecure_skip_verify: bool

class PrometheusConfig(BaseModel):
    enabled: bool
    url: HttpUrl
    query_timeout: str = Field(pattern=r"^\d+[smhd]$")  # Supports 30s, 1m, 1h formats
    query: str
    tls_config: Optional[TLSConfig]


class DataSourceSystemConfig(BaseModel):
    path: str
    data_sources: Optional[Dict[str, PrometheusConfig]]


class AppConfig(BaseModel):
    data_sources: DataSourceSystemConfig
    parsers: ParserSystemConfig
