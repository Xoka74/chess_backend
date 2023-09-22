from dataclasses import dataclass


@dataclass
class BotResponse:
    board: str
    status: int
