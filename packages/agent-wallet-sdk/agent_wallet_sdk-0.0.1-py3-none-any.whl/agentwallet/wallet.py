from typing import List, Optional
from dataclasses import dataclass, field

from .api_client import ApiClient
from .transaction import Transaction


@dataclass
class Card:
    card_name: str
    card_number: str
    expiry: str
    cvv: str


@dataclass
class Wallet:
    _api_client: ApiClient = field(repr=False, compare=False)
    wallet_uid: str
    transactions: Optional[List[Transaction]] = None
    balance_usd_cents: Optional[int] = None

    def transfer(self, transfer_to: str, amount_usd_cents: int) -> bool:
        data = {
            "transfer_to_user_email": transfer_to,
            "amount_usd_cents": amount_usd_cents,
        }
        response = self._api_client.post(
            f"wallet/{self.wallet_uid}/transfer", data=data
        )
        return response["response"] == "OK"

    def balance(self) -> int:
        response = self._api_client.get(f"wallets/{self.wallet_uid}")
        self.balance_usd_cents = response["wallet"]["balance_usd_cents"]
        return self.balance_usd_cents

    def get_card(self, agent_name: str) -> Optional[Card]:
        url = f"wallets/{self.wallet_uid}/card?card_name={agent_name}"
        response = self._api_client.get(url)
        if response:
            card_dict = response["card"]
            return Card(
                card_name=card_dict["card_name"],
                card_number=card_dict["card_number"],
                expiry=card_dict["expiry"],
                cvv=card_dict["cvv"],
            )
