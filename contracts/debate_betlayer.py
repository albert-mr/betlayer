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
        if position not in self.VALID_POSITIONS:
            raise Exception(
                f"Invalid position '{position}'. Must be one of: {', '.join(sorted(self.VALID_POSITIONS))}"
            )

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

    @gl.public.write
    def resolve_debate(self) -> None:
        # Gather arguments by position
        for_arguments = []
        against_arguments = []
        neutral_arguments = []

        for bet in self.bets:
            if bet.argument.strip():  # Only include non-empty arguments
                if bet.position == "for":
                    for_arguments.append(bet.argument)
                elif bet.position == "against":
                    against_arguments.append(bet.argument)
                elif bet.position == "neutral":
                    neutral_arguments.append(bet.argument)

        # Format arguments for prompt
        for_args_text = (
            "\n".join(for_arguments) if for_arguments else "No arguments provided"
        )
        against_args_text = (
            "\n".join(against_arguments)
            if against_arguments
            else "No arguments provided"
        )
        neutral_args_text = (
            "\n".join(neutral_arguments)
            if neutral_arguments
            else "No arguments provided"
        )

        prompt = f"""
You are a debate resolutor bot. You are given an assertion and arguments. 
Arguments are either for, against or neutral to the assertion.
You need to analyze all arguments objectively and determine the winning position based on the strength of the arguments.

The assertion is: {self.assertion}

The arguments in favor of the assertion are:
{for_args_text}

The arguments against the assertion are:
{against_args_text}

The arguments neutral to the assertion are:
{neutral_args_text}

Analyze each argument carefully and determine which position has the strongest case. Consider:
1. Quality and validity of arguments
2. Evidence provided
3. Logical reasoning
4. Factual accuracy

Respond using ONLY the following format:
{{
"reasoning": str,
"winning_position": str
}}

VALID_POSITIONS = {{"for", "against", "neutral"}}
It is mandatory that you respond only using the JSON format above,
nothing else. Don't include any other words or characters,
your output must be only JSON without any formatting prefix or suffix.
This result should be perfectly parseable by a JSON parser without errors.
"""

        def get_debate_resolution():
            result = gl.nondet.exec_prompt(prompt)
            result = result.replace("```json", "").replace("```", "")
            print(result)
            return result

        result = gl.eq_principle.prompt_comparative(
            get_debate_resolution, "The value of winning_position has to match"
        )
        parsed_result = json.loads(result)
        assert isinstance(parsed_result["winning_position"], str)
        assert parsed_result["winning_position"] in self.VALID_POSITIONS
        self.resolution = parsed_result["winning_position"]
        self.is_resolved = True

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
