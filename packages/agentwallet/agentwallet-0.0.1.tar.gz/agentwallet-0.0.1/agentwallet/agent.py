from urllib.parse import urljoin
from dataclasses import dataclass, field

from .api_client import ApiClient
from .api_client import AGENT_WALLET_BASE_URL


@dataclass
class Agent:
    _api_client: ApiClient = field(repr=False, compare=False)
    endpoint_id: str
    name: str
    description: str
    author: str
    price_usd_cents: int

    @property
    def base_url(self):
        return urljoin(AGENT_WALLET_BASE_URL, f"agents/{self.name}")
