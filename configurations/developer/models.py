from typing import Optional, Dict

from pydantic import BaseModel, HttpUrl, Field


class ParserConfig(BaseModel):
    enabled: bool

class ParserSystemConfig(BaseModel):
    enabled: bool
    path: str
    parsers: Optional[Dict[str, ParserConfig]]


class AnalyzerConfig(BaseModel):
    enabled: bool


class TrainerConfig(BaseModel):
    enabled: bool


class AnalyzerSystemConfig(BaseModel):
    enabled: bool
    path: str
    analyzers: Optional[Dict[str, AnalyzerConfig]]


class TrainerSystemConfig(BaseModel):
    enabled: bool
    path: str
    trainers: Optional[Dict[str, TrainerConfig]]


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
    datasources: Optional[Dict[str, PrometheusConfig]]


class AppConfig(BaseModel):
    datasources: DataSourceSystemConfig
    parsers: ParserSystemConfig
    trainers: TrainerSystemConfig
    analyzers: AnalyzerSystemConfig
