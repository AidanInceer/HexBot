from dataclasses import dataclass


@dataclass
class Cards:
    knight: int = 0
    victory_point: int = 0
    monopoly: int = 0
    road_building: int = 0
    year_of_plenty: int = 0

    def __repr__(self) -> str:
        cards = []
        types = [
            "knight",
            "victory_point",
            "monopoly",
            "road_building",
            "year_of_plenty",
        ]
        for card in types:
            if getattr(self, card) > 0:
                cards.append(f"{card}: {getattr(self, card)}")
        if len(cards) == 0:
            cards = "None"
        else:
            cards = ", ".join(cards)

        return f"Cards: {cards}"
