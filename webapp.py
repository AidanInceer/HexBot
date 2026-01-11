
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

        with ui.row().classes("w-full max-w-7xl gap-4"):
            # Left Column: Game Board
            with ui.card().classes("w-2/3 h-[600px] bg-gray-800 border-gray-700").style(f"background-color: {Palette.WATER}"):
                # Container for SVG
                board_container = ui.element("div").classes("w-full h-full flex items-center justify-center")
                renderer = HexGridRenderer(board_container)

            # Right Column: Controls & Log
            with ui.column().classes("w-1/3 gap-4"):
                # Input Area
                with ui.card().classes("w-full bg-gray-800 border-gray-700 p-4"):
                    ui.label("Actions").classes("text-xl font-bold mb-2")
                    input_container = ui.column().classes("w-full gap-2")

                # Log Area
                with ui.card().classes("w-full h-96 bg-gray-800 border-gray-700 flex-grow"):
                    ui.label("Game Log").classes("text-sm text-gray-400 mb-2")
                    log_view = ui.log().classes("w-full h-full text-sm font-mono")

    # State processing
    def process_updates():
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
                ui.label(req["message"]).classes("text-lg")

                vals = req["value_range"]

                def make_choice(v):
                    bridge.input_response_queue.put(v)
                    input_container.clear()
                    ui.spinner("dots")  # Show waiting state

                # Basic heuristic for input type
                if len(vals) < 15:
                    # Buttons for small sets
                    with ui.row().classes("flex-wrap gap-2"):
                        for v in vals:
                            ui.button(str(v), on_click=lambda v=v: make_choice(v)).props("outline color=accent")
                else:
                    # Dropdown for large sets
                    ui.select(options=vals, on_change=lambda e: make_choice(e.value)).props(
                        'label="Select Option" color=accent'
                    ).classes("w-full")

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
