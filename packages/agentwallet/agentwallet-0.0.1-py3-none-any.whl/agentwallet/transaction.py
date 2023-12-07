from dataclasses import dataclass


@dataclass
class Transaction:
    transfer_from: str
    transfer_to: str
    amount_usd_cents: int
    status: str
