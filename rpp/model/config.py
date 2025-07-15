import os
from typing import List, Optional
import yaml
from pydantic_settings import BaseSettings

class Config(BaseSettings):

    rpp_epp_host: str
    rpp_epp_port: Optional[int] = 700
    rpp_epp_use_tls: Optional[bool] = True
    rpp_epp_timeout: Optional[float] = 5.0

    rpp_epp_objects: List[str] = [
        'urn:ietf:params:xml:ns:domain-1.0',
        'urn:ietf:params:xml:ns:contact-1.0',
        'urn:ietf:params:xml:ns:host-1.0',
    ]

    rpp_epp_extensions: Optional[List[str]] = None
    rpp_epp_connection_cache: Optional[bool] = False

    rpp_epp_ns_map: Optional[dict[str, str]] = {}

    def __init__(self, **kwargs):
        if not kwargs:
            config_path = os.getenv("RPP_CONFIG_FILE", "config.yaml")
            with open(config_path) as f:
                data = yaml.safe_load(f)
            super().__init__(**data)
        else:
            super().__init__(**kwargs)
