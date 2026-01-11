from nicegui import ui


class Palette:
    # Resources
    WOOD = "#228B22"  # ForestGreen
    BRIGK = "#B22222"  # FireBrick
    SHEEP = "#90EE90"  # LightGreen (Pasture)
    WHEAT = "#DAA520"  # GoldenRod
    ORE = "#708090"  # SlateGray
    DESERT = "#F4A460"  # SandyBrown
    WATER = "#4682B4"  # SteelBlue

    # Players
    PLAYER_RED = "#FF4444"
    PLAYER_BLUE = "#4444FF"
    PLAYER_GREEN = "#44FF44"
    PLAYER_YELLOW = "#FFFF44"

    # UI
    BACKGROUND = "#1a1a1a"
    TEXT = "#ffffff"
    HIGHLIGHT = "#ffffff"

    @staticmethod
    def get_tile_color(tile_type_name: str):
        mapping = {
            "Forest": Palette.WOOD,
            "Hills": Palette.BRIGK,
            "Pasture": Palette.SHEEP,
            "Fields": Palette.WHEAT,
            "Mountains": Palette.ORE,
            "Desert": Palette.DESERT,
        }
        return mapping.get(tile_type_name, "#333333")

    @staticmethod
    def get_player_color(color_name: str):
        return getattr(Palette, f"PLAYER_{color_name.upper()}", "#cccccc")
