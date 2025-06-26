import os
import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='rpp_')

    epp_host: str
    epp_port: int = 700
    epp_use_tls: bool = True
    epp_timeout: float = 5.0
    epp_client_id: str
    epp_password: str
