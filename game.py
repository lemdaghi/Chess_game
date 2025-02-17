import pygame
import time
import threading

from ai import AIPlayer  # Import the AI logic

from board import Board
from chess_rules import ChessRules

class Game:
    def __init__(self, mode="2_players", time_control = "rapid"):
        self.board = Board()
        self.current_player = "white"
        self.game_over = False
        self.move_history = []
        self.history = []
        self.count_moves = 0
        self.mode = mode

        # Define available time controls
        self.time_options = {
            "bullet": 60,  # 1 minutes (60 sec)
            "blitz": 300,   # 5 minutes (300 sec) [DEFAULT]
            "rapid": 600,  # 10 minutes (600 sec)
            "classical": 3600  # 1 hour (3600 sec)
        }

        # Initialize player clocks (10 minutes each)
        self.time_control = self.time_options.get(time_control, 600)
        self.player_timers = {"white": self.time_control, "black": self.time_control}

        # Start the clock
        self.running = True
        self.clock_thread = threading.Thread(target=self.run_clock)
        self.clock_thread.daemon = True
        self.clock_thread.start()

    def handle_click(self, position):
        if self.game_over:
            print("🚫 Game is Over.")
            self.propose_rematch()
            return
        
        x, y = position[0] // 75, position[1] // 75
        clicked_piece = self.board.get_piece((x, y))

        if self.board.selected_piece:
            if (x, y) in self.board.valid_moves:
                old_position = self.board.selected_piece.position
                self.history.append((self.board.copy(), self.count_moves)) # save board before moving
                self.print_board(self.board)

                legal_move = self.board.move_piece(self.board.selected_piece, (x, y))

                if legal_move:
                    move_description = f"{self.board.selected_piece.symbol} {self.board.pos_to_chess_notation(old_position)} → {self.board.pos_to_chess_notation((x, y))}"
                    self.move_history.append(move_description)
                    print(move_description)

                    print("New chessboard :")
                    self.print_board(self.board)

                    # Update move counter
                    if self.board.selected_piece.__class__.__name__ == "Pawn" or (clicked_piece is not None and clicked_piece.color != self.board.get_piece((x, y)).color):
                        self.count_moves = 0
                    else:
                        self.count_moves += 1  # Normal increase

                    print(f"⏳ 50 Moves Rule: {self.count_moves}/100")

                    self.board.record_position()  # save position
                    self.switch_turn()
                    self.check_victory()
                else:
                    print("🚫 Illegal move !")
            self.board.selected_piece = None
            self.board.valid_moves = []

        elif clicked_piece and clicked_piece.color == self.current_player: # We just selected a piece, making sure the player selected his own pieces
            self.board.selected_piece = clicked_piece
            self.board.valid_moves = [move for move in clicked_piece.get_moves(self.board) if self.board.check_legal_move(clicked_piece, move)]
        
    def switch_turn(self):
        self.current_player = "white" if self.current_player == "black" else "black"

        if self.mode == "vs_ai" and self.current_player == "black":
            print("AI is thinking...")
            self.ai_move()  # AI plays automatically
        
        # Print the updated time after switching turns
        self.display_time()

    def ai_move(self):
        """AI selects and plays a move."""
        
        ai_player = AIPlayer(self.board, "black")
        best_move = ai_player.get_best_move()  # Assume AIPlayer has a function to get the best move
        if best_move:
            piece, new_position = best_move
            old_position = piece.position
            clicked_piece = self.board.get_piece(new_position)

            self.history.append((self.board.copy(), self.count_moves)) # save board before moving
            self.print_board(self.board)

            self.board.move_piece(piece, new_position)
            move_description = f"{piece.symbol} {self.board.pos_to_chess_notation(old_position)} → {self.board.pos_to_chess_notation(new_position)}"
            self.move_history.append(move_description)
            print(move_description)

            print("New chessboard :")
            self.print_board(self.board)

            # Update move counter
            if piece.__class__.__name__ == "Pawn" or (clicked_piece is not None and clicked_piece.color != self.board.get_piece(new_position).color):
                self.count_moves = 0
            else:
                self.count_moves += 1  # Normal increase

            print(f"⏳ 50 Moves Rule: {self.count_moves}/100")

            self.board.record_position()  # Save position

            self.check_victory()
            self.switch_turn()

    def print_board(self, board):
        """Displays the chessboard in the terminal for debugging."""
        print("\n   a b c d e f g h")
        print("  -----------------")
        for y in range(8):
            row_str = f"{8 - y} | "
            for x in range(8):
                piece = board.grid[y][x]
                row_str += piece.symbol if piece else "·"
                row_str += " "
            print(row_str + f"| {8 - y}")
        print("  -----------------")
        print("   a b c d e f g h\n")

    def get_move_history(self):
        """Returns the history of moves played."""
        return self.move_history
    
    def run_clock(self):
        """Runs the chess clock for both players."""
        while self.running and not self.game_over:
            time.sleep(1)  # Wait for 1 second
            if not self.game_over:
                self.player_timers[self.current_player] -= 1

                # If a player runs out of time, they lose
                if self.player_timers[self.current_player] <= 0:
                    print(f"⏳ {self.current_player.capitalize()} ran out of time! Game Over.")
                    opponent = "white" if self.current_player == "black" else "black"
                    print(f"⏳🏆 {opponent.capitalize()} Wins by time !")
                    self.game_over = True
                    break  # Stop the clock

                # 🕰️ Display remaining time
                self.display_time()

    def display_time(self):
        """Displays the remaining time for each player."""
        white_time = self.format_time(self.player_timers["white"])
        black_time = self.format_time(self.player_timers["black"])
        print(f"⏳ White: {white_time} | Black: {black_time}")

    def format_time(self, seconds):
        """Formats the time as MM:SS."""
        minutes = seconds // 60
        sec = seconds % 60
        return f"{minutes:02}:{sec:02}"

    def undo_move(self):
        if self.game_over:
            print("Game is over, You can not undo anymore !")
            self.propose_rematch()
            return

        if self.history:
            print("📜 Last saved state before undo :")
            self.print_board(self.history[-1][0])

            last_board, last_count_moves = self.history.pop()  # Restore thr grid before last move

            self.board.grid = last_board.grid
            self.current_player = "white" if self.current_player == "black" else "black"
            self.count_moves = last_count_moves
            
            print(f"⏳ 50 Moves Rule after undo : {self.count_moves}/100")

            # Delete the last position_history state to avoid repetition errors
            if isinstance(self.board.position_history, dict) and self.board.position_history:
                last_key = list(self.board.position_history.keys())[-1]  # Recover last key (Python Version >= 3.7, dictionaries retain the order in which they were added)
                print(f"🗑 Delete last saved position : {last_key}")
                self.board.position_history.pop(last_key)

            # DEBUG : Display tray state after undo
            print("🔙 Grid state after undo :")
            self.print_board(self.board)

            if self.move_history:
                self.move_history.pop()
            print("🔄 Undo : Last move has been canceled.")
        else:
            print("🚫 No moves to cancel.")

    def restart_game(self):
        self.board = Board()  # Resets chessboard
        self.current_player = "white"
        self.game_over = False
        self.move_history = []
        self.history = []  # Clear history
        self.count_moves = 0
        print("🔄 The game has been restarted.")

    def propose_rematch(self):
        """Propose a rematch and reset the game if accepted."""
        response = input("🔄 Do you want a rematch? (yes/no): ").strip().lower()
        if response == "yes":
            self.restart_game()
        else:
            print("🎉 Game over! Thanks for playing!")


    def is_fifty_move_rule(self):
        """Returns True if the fifty move rule applies."""
        if self.count_moves >= 100:
            print("⚖️ Draw by fifty move rule !")
            return True
        return False


    def check_victory(self):
        """Checks whether the game has ended in checkmate."""
        if ChessRules.is_checkmate(self.board, "white"):
            print("🏆 Black wins by checkmate !")
            self.game_over = True
            return
        elif ChessRules.is_checkmate(self.board, "black"):
            print("🏆 White wins by checkmate !")
            self.game_over = True
            return
        
        if ChessRules.is_stalemate(self.board, self.current_player):
            print("⚖️ Draw by stalemate !")
            self.game_over = True
            return

        if ChessRules.is_insufficient_material(self.board):
            print("⚖️ Draw by insufficient material !")
            self.game_over = True
            return
        
        if self.board.is_triple_repetition():
            print("⚖️ Draw by threefold !")
            self.game_over = True
            return
        
        if self.is_fifty_move_rule():
            print("⚖️ Draw by fifty move rule !")
            self.game_over = True
            return
        
        # Stop the clock if the game is over
        if self.game_over:
            self.running = False

        