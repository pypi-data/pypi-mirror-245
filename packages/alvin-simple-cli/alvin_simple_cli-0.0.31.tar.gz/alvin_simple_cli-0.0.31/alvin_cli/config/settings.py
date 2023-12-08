import os
from typing import Optional

from dotenv import load_dotenv

from alvin_cli.config.loader import load_cfg_file


class Settings:
    alvin_api_host: str = "https://app.alvin.ai"
    alvin_dbt_api_url: str = "https://dbt.alvin.ai"
    alvin_api_token: Optional[str] = None
    alvin_verbose_log: bool = False
    alvin_datafakehouse_api_url: str = "datafakehouse-3ggwwp7l3q-ey.a.run.app:443"

    def __init__(self) -> None:

        cfg_file = load_cfg_file()

        if not cfg_file:
            load_dotenv(f"{os.getcwd()}/.env")
            kwargs = {
                "alvin_api_host": os.getenv("ALVIN_API_HOST", "https://app.alvin.ai"),
                "alvin_api_token": os.getenv("ALVIN_API_TOKEN", ""),
                "alvin_verbose_log": os.getenv("ALVIN_VERBOSE_LOG", "false"),
                "alvin_dbt_api_url": os.environ.get("ALVIN_DBT_API_URL", "https://dbt.alvin.ai"),
                "alvin_datafakehouse_api_url": os.environ.get(
                    "ALVIN_DATAFAKEHOUSE_API_URL",
                    "datafakehouse-3ggwwp7l3q-ey.a.run.app:443",
                ),
            }
        else:
            kwargs = cfg_file

        self.alvin_api_host = kwargs.get("alvin_api_host") or ""
        self.alvin_dbt_api_url = kwargs.get("alvin_dbt_api_url") or ""
        self.alvin_api_token = kwargs.get("alvin_api_token") or ""
        alvin_verbose_log = kwargs.get("alvin_verbose_log") or ""
        self.alvin_verbose_log = alvin_verbose_log.lower() == "true" if alvin_verbose_log else False
        self.alvin_datafakehouse_api_url = kwargs.get("alvin_datafakehouse_api_url") or ""

