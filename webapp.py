
import threading
import queue
import traceback
from nicegui import ui, app

from src.catan.game.game import Game
from src.catan.board.board import Board
from src.catan.deck.deck import CardDeck
from src.catan.player.player import Player
from src.config.config import load_config
from src.utils.handlers import PathHandler
from src.interface.web.renderer import HexGridRenderer
from src.interface.web.styles import Palette
from src.interface.web.bridge import GameBridge
from src.interface.web.handlers import WebDisplayHandler, WebInputHandler

# --- Initialization ---
# Create the synchronized bridge instance
bridge = GameBridge()

# --- Game Thread ---
def game_thread_func():
    try:
        config = load_config(PathHandler.config_path)
        deck = CardDeck().generate_dev_cards()
        board = Board()
        board.generate()

        # Initial render push
        # print("Initial board generated, pushing update...")
        bridge.push_board_update(board)

        game = Game(
            players=[
                Player(name=0, color="Red", type="human"),
                Player(name=1, color="Yellow", type="bot"),
                Player(name=2, color="Blue", type="bot"),
                Player(name=3, color="Green", type="bot"),
            ],
            deck=deck,
            board=board,
            game_type="AUTO_SETUP",
            config=config,
            display_handler=WebDisplayHandler(bridge),
            input_handler=WebInputHandler(bridge),
        )
        game.run()
    except Exception as e:
        error_msg = f"Game Error: {e}\n{traceback.format_exc()}"
        print(error_msg)
        bridge.push_msg(error_msg)


# --- UI (Main Thread) ---
@ui.page("/")
def index():
    # Style setup
    ui.colors(primary=Palette.WATER, secondary=Palette.WHEAT, accent=Palette.WOOD, dark=Palette.BACKGROUND)

    with ui.column().classes("w-full h-screen items-center justify-center bg-gray-900 text-white p-4"):
        ui.label("HexBot - Catan").classes("text-4xl font-bold mb-4 text-amber-500")

        with ui.row().classes("w-full max-w-7xl gap-4 items-start justify-center"):
            # Left Column: Game Board
            with ui.column().classes("w-1/2 gap-4"):
                with ui.card().classes("w-full h-[600px] bg-gray-800 border-gray-700").style(f"background-color: {Palette.WATER}"):
                    # Container for SVG
                    board_container = ui.element("div").classes("w-full h-full flex items-center justify-center")
                    renderer = HexGridRenderer(board_container)
                
                # Legend
                with ui.card().classes("w-full bg-gray-800 border-gray-700 p-2"):
                    ui.label("Terrain Key").classes("text-sm font-bold text-gray-400 mb-2")
                    with ui.row().classes("gap-4 flex-wrap"):
                        legend_items = [
                            ("Forest", Palette.WOOD),
                            ("Hills", Palette.BRICK), 
                            ("Pasture", Palette.SHEEP),
                            ("Fields", Palette.WHEAT),
                            ("Mountains", Palette.ORE),
                            ("Desert", Palette.DESERT)
                        ]
                        for name, color in legend_items:
                            with ui.row().classes("items-center gap-2"):
                                ui.element("div").classes("w-4 h-4 rounded-full").style(f"background-color: {color}; border: 1px solid white;")
                                ui.label(name).classes("text-xs")

            # Right Column: Controls & Log
            with ui.column().classes("w-1/2 gap-4 h-[600px]"):
                # Input Area
                with ui.card().classes("w-full bg-gray-800 border-gray-700 p-4 min-h-[150px]"):
                    ui.label("Actions").classes("text-xl font-bold mb-2")
                    input_container = ui.column().classes("w-full gap-2")

                # Log Area
                with ui.card().classes("w-full bg-gray-800 border-gray-700 flex-grow"):
                    ui.label("Game Log").classes("text-sm text-gray-400 mb-2")
                    log_view = ui.log().classes("w-full h-full text-sm font-mono p-2")

    def parse_options(message: str, values: list):
        """
        Parses the message string to map value integers to labels.
        Example: "1=Build, 2=Trade" -> {1: "Build", 2: "Trade"}
        """
        import re
        options = {}
        # improved regex to capture "1=Something With Spaces," or "1=Build"
        # look for digit=... until comma or end of string
        matches = re.findall(r'(\d+)=([^,]+)', message)
        
        valid_map = {}
        for val_str, label in matches:
            try:
                val = int(val_str)
                if val in values:
                    valid_map[val] = label.strip()
            except ValueError:
                pass
        
        return valid_map

    # State processing
    def process_updates():
        try:
            # Display Updates
            while not bridge.display_queue.empty():
                type_, data = bridge.display_queue.get()
                if type_ == "msg":
                    log_view.push(data)
                elif type_ == "board":
                    # Render the board using the new renderer
                    renderer.render_board(data)

            # Input Requests
            if not bridge.input_request_queue.empty():
                req = bridge.input_request_queue.get()
                with input_container:
                    input_container.clear()
                    
                    # Check if we can parse labels from the message
                    message = req["message"]
                    vals = req["value_range"]
                    
                    parsed_labels = parse_options(message, vals)
                    
                    ui.label(message).classes("text-lg mb-2")

                    def make_choice(v):
                        bridge.input_response_queue.put(v)
                        input_container.clear()
                        ui.spinner("dots")  # Show waiting state

                    # Basic heuristic for input type
                    if len(vals) < 15:
                        # Buttons for small sets
                        with ui.row().classes("flex-wrap gap-2"):
                            for v in vals:
                                label = parsed_labels.get(v, str(v))
                                ui.button(label, on_click=lambda v=v: make_choice(v)).props("outline color=accent").classes("min-w-[40px]")
                    else:
                        # Dropdown for large sets
                        # Use parsed labels if available
                        options_dict = {v: parsed_labels.get(v, str(v)) for v in vals}
                        ui.select(options=options_dict, on_change=lambda e: make_choice(e.value)).props(
                            'label="Select Option" color=accent'
                        ).classes("w-full")
        except Exception as e:
            print(f"Error in process_updates: {e}\n{traceback.format_exc()}")
            ui.notify(f"UI Error: {e}", type="negative")

    ui.timer(0.1, process_updates)

    def start_game():
        # Start thread
        t = threading.Thread(target=game_thread_func, daemon=True)
        t.start()
        input_container.clear()
        ui.label("Game Started...").classes("animate-pulse text-green-400")

    # Initial Start Button
    with input_container:
        ui.button("Start Game", on_click=start_game).props("size=lg icon=play color=green")


ui.run(title="HexBot", port=8080, reload=False, dark=True)
