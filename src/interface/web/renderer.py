import math
from nicegui import ui
from src.interface.web.styles import Palette


class HexGridRenderer:
    def __init__(self, container):
        self.container = container
        self.hex_radius = 50
        self.width = 800
        self.height = 600
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        self.svg = None

        # Hardcoded layout for 19 tiles (3-4-5-4-3)
        # q, r axial coordinates or just row/col offset
        # Let's use simple row offsets
        self.layout = [
            (0, -2, 3),  # Row 0: y=-2, 3 tiles
            (1, -1, 4),  # Row 1: y=-1, 4 tiles
            (2, 0, 5),  # Row 2: y=0,  5 tiles
            (3, 1, 4),  # Row 3: y=1,  4 tiles
            (4, 2, 3),  # Row 4: y=2,  3 tiles
        ]

        # Mapping tile_id -> (x, y) center pixel
        self.tile_positions = {}

    def render_board(self, board):
        print(f"Rendering board with {len(board.tiles)} tiles")
        self.container.clear()
        with self.container:
            with ui.element("svg").props(
                f'viewBox="0 0 {self.width} {self.height}" width="{self.width}" height="{self.height}"'
            ) as svg:
                self.svg = svg
                self._draw_tiles(board)
                self._draw_roads(board)
                self._draw_settlements(board)

    def _draw_tiles(self, board):
        tile_id_counter = 0

        # Calculate positions
        # Hex height = 2 * radius
        # Hex width = sqrt(3) * radius
        # Vertical distance between rows = 3/2 * radius
        # Horizontal distance = width

        w = math.sqrt(3) * self.hex_radius
        h = 2 * self.hex_radius
        vert_dist = 1.5 * self.hex_radius
        horiz_dist = w

        for row_idx, y_offset, count in self.layout:
            # Center the row
            row_width = count * horiz_dist
            start_x = self.center_x - (row_width / 2) + (horiz_dist / 2)
            y = self.center_y + (y_offset * vert_dist)

            for i in range(count):
                x = start_x + (i * horiz_dist)

                if tile_id_counter < len(board.tiles):
                    tile = board.tiles[tile_id_counter]
                    self.tile_positions[tile.id] = (x, y)
                    self._draw_hex(x, y, tile)
                    tile_id_counter += 1

    def _draw_hex(self, x, y, tile):
        # Draw Polygon
        points = []
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.pi / 180 * angle_deg
            px = x + self.hex_radius * math.cos(angle_rad)
            py = y + self.hex_radius * math.sin(angle_rad)
            points.append(f"{px},{py}")

        color = Palette.get_tile_color(type(tile.type).__name__)

        # Hexagon
        ui.element("polygon").props(f'points="{" ".join(points)}" fill="{color}" stroke="black" stroke-width="2"')

        # Token / Number
        if tile.token:
            ui.element("circle").props(f'cx="{x}" cy="{y}" r="15" fill="white"')
            t = ui.element("text").props(f'x="{x}" y="{y}" text-anchor="middle" dy=".3em" font-weight="bold"')
            t.text = str(tile.token)

        # Robber
        if tile.robber:
            ui.element("circle").props(f'cx="{x}" cy="{y + 20}" r="10" fill="black"')

    def _draw_roads(self, board):
        # Simplification: We need edge mapping to coordinates.
        # For now, just a placeholder or we iterate abstract edges if we can map them to nodes.
        pass

    def _draw_settlements(self, board):
        pass
