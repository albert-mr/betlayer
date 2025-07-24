# v0.1.0
# { "Depends": "py-genlayer:latest" }

import json
import uuid
from dataclasses import dataclass
from typing import List

from genlayer import *


@allow_storage
@dataclass
class Bet:
    id: str
    bettor: str
    amount: str
    argument: str
    position: str


class Debate_BetLayer(gl.Contract):
    # Valid betting positions
    VALID_POSITIONS = {"for", "against", "neutral"}

    owner: Address
    assertion: str
    is_resolved: bool
    resolution: str
    total_pool: bigint
    for_pool: bigint
    against_pool: bigint
    neutral_pool: bigint
    bets: DynArray[Bet]

    def __init__(
        self,
        assertion: str,
    ):
        self.owner = gl.message.sender_address
        self.assertion = assertion
        self.is_resolved = False
        self.resolution = ""
        self.bets = []

    @gl.public.write
    def place_bet(
        self,
        position: str,
        amount: str,
        argument: str = "",
    ) -> str:
        # Validate position early
        if position not in self.VALID_POSITIONS:
            raise Exception(
                f"Invalid position '{position}'. Must be one of: {', '.join(sorted(self.VALID_POSITIONS))}"
            )

        # Validate amount
        try:
            amount_int = int(amount)
            if amount_int <= 0:
                raise Exception("Bet amount must be positive")
        except ValueError:
            raise Exception("Invalid amount format")

        sender_address = gl.message.sender_address

        bet = Bet(
            id=str(uuid.uuid4()),
            bettor=str(sender_address),
            amount=amount,
            argument=argument,
            position=position,
        )
        self.bets.append(bet)

        # Update pools using dictionary mapping for cleaner code
        pool_mapping = {
            "for": lambda: setattr(self, "for_pool", self.for_pool + amount_int),
            "against": lambda: setattr(
                self, "against_pool", self.against_pool + amount_int
            ),
            "neutral": lambda: setattr(
                self, "neutral_pool", self.neutral_pool + amount_int
            ),
        }

        self.total_pool += amount_int
        pool_mapping[position]()

        return bet.id

    @gl.public.view
    def get_bets(self) -> List[Bet]:
        return self.bets

    @gl.public.view
    def get_bet(self, bet_id: str) -> Bet:
        return next((bet for bet in self.bets if bet.id == bet_id), None)

    @gl.public.view
    def get_assertion(self) -> str:
        return self.assertion

    @gl.public.view
    def get_pools(self) -> str:
        return {
            "total_pool": str(self.total_pool),
            "for_pool": str(self.for_pool),
            "against_pool": str(self.against_pool),
            "neutral_pool": str(self.neutral_pool),
        }
