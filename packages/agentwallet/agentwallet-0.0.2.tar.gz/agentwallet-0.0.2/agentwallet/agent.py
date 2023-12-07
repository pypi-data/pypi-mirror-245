from typing import Optional
from urllib.parse import urljoin
from enum import Enum
from dataclasses import dataclass, field

from .api_client import ApiClient
from .api_client import AGENT_WALLET_BASE_URL


class AgentType(str, Enum):
    OPENAI = "OPENAI"
    AGENTPROTOCOL = "AGENTPROTOCOL"
    SUPERAGENT_SH = "SUPERAGENT_SH"


@dataclass
class Agent:
    _api_client: ApiClient = field(repr=False, compare=False)
    wallet_id: str
    type: AgentType
    authorization: Optional[str]
    url: str
    endpoint_id: str
    name: str
    description: str
    author: str
    price_usd_cents: int

    @property
    def base_url(self):
        return urljoin(AGENT_WALLET_BASE_URL, f"agents/{self.name}")
