class ChessRules:

    @staticmethod
    def is_in_check(board, color, position=None, ignore_castling=False):
        """Return True if the 'color' king is checked, unless the check for Castle is ignored."""
        king_pos = None
        
        if position:
            king_pos = position
        else:
            for row in board.grid:
                for piece in row:
                    if piece and piece.__class__.__name__ == "King" and piece.color == color:
                        king_pos = piece.position
                        break

        if not king_pos:
            print("🚨 ERROR: King not found !")
            return False
          
        x, y = king_pos

        # Simulate removing the piece
        temp_piece = board.get_piece(king_pos)
        board.grid[y][x] = None 
        
        # Verify all opponent pieces
        in_check = False
        for row in board.grid:
            for piece in row:
                if piece and piece.color != color and piece.__class__.__name__ != "King":
                    # Special verification for Pawns
                    if piece.__class__.__name__ == "Pawn":
                        direction = -1 if piece.color == "white" else 1  # White goes up, Black goes down
                        for dx in [-1, 1]:  # Diagonal attack
                            px, py = piece.position
                            if (px + dx, py + direction) == (x, y):  # The King is on an attacked square
                                in_check = True
                                break
                    elif king_pos in piece.get_moves(board, simulate=True):
                        in_check = True
                        break  
                    
        # Restore initial state
        board.grid[y][x] = temp_piece
        return in_check  

    @staticmethod
    def is_checkmate(board, color):
        """Return True if 'color' player is Checkmate."""
        if not ChessRules.is_in_check(board, color):
            return False  # No Check, no Checkmate.

        king = None
        for row in board.grid:
            for piece in row:
                if piece and piece.__class__.__name__ == "King" and piece.color == color:
                    king = piece

        if king is None:
            print("🚨 ERROR: King not found !")
            return False  

        print(f"⚠️ {color} King is checked !")
        # 1️⃣ Verify if king can escape
        original_position = king.position  # Save king's initial position
        for move in king.get_moves(board):  # Test every possible move
            # Simulate the move
            target_piece = board.get_piece(move) 
            board.grid[original_position[1]][original_position[0]] = None 
            board.grid[move[1]][move[0]] = king  
            king.position = move 

            print(f"Testing move: King moves to {move}")

            if not ChessRules.is_in_check(board, color):  
                print(f"King escapes check by moving to {move}")
                # King can escape no checkmate, we restore initial state
                board.grid[move[1]][move[0]] = target_piece  
                board.grid[original_position[1]][original_position[0]] = king 
                king.position = original_position  
                return False 
            
            # Restore initial state after every move
            board.grid[move[1]][move[0]] = target_piece  
            board.grid[original_position[1]][original_position[0]] = king  
            king.position = original_position 

        print(f"{color.capitalize()} King is checked and has no escape!")

        # 2️⃣ Verify if another piece can capture or parry the attacker piece
        attackers = []
        for row in board.grid:
            for piece in row:
                if piece and piece.color != color:
                    if king.position in piece.get_moves(board, simulate=True):  
                        attackers.append(piece)

        if len(attackers) > 1:
            return True  # If many attackers (more than one) are checking the king, and he can not escape -> checkmate

        attacker = attackers[0]  # There is only 1 attacker

        # 3️⃣ Check whether an allied piece can capture the attacker
        for row in board.grid:
            for piece in row:
                if piece and piece.color == color:
                    if attacker.position in piece.get_moves(board, simulate=True):  
                        return False

        # 4️⃣ Check whether an allied piece can parry the attacker
        if attacker.__class__.__name__ != "Knight":  # Knight attack can not be parried
            print(f"attacker is {attacker.__class__.__name__}")
            x1, y1 = king.position
            x2, y2 = attacker.position
            path = []  

            dx = (x2 - x1) // max(1, abs(x2 - x1))  
            dy = (y2 - y1) // max(1, abs(y2 - y1))  

            nx, ny = x1 + dx, y1 + dy
            while (nx, ny) != (x2, y2):
                path.append((nx, ny))
                nx += dx
                ny += dy

            for row in board.grid:
                for piece in row:
                    if piece and piece.color == color:
                        for move in piece.get_moves(board, simulate=True):  
                            if move in path:
                                return False  # A piece can parry the attack

        return True  # Nothing can save the king -> Checkmate

    @staticmethod
    def is_stalemate(board, color):
        """Verify if the `color` player is stalemate."""
        if ChessRules.is_in_check(board, color):
            return False  # If Check, no Stalemate

        # Browse all player's pieces
        for row in board.grid:
            for piece in row:
                if piece and piece.color == color:
                    valid_moves = piece.get_moves(board)  # Recover legal moves
                    
                    for move in valid_moves[:]:  # Use a copy
                        if board.check_legal_move(piece, move):  
                            return False  # Still at least 1 legal move → No stalemate
                    
        print("⚖️ Draw by stalemate ! No legal move possible.")
        return True  # No legal move -> stalemate

    @staticmethod
    def is_insufficient_material(board):
        """Return True if there is not enough pieces to checkmate."""
        pieces = []
        bishops = {"light": 0, "dark": 0}
        has_other_piece = False  # To detect Rook, Queen, Pawn, Knight

        for row in board.grid:
            for piece in row:
                if piece:
                    pieces.append(piece)

                    # Fast verification : if a Rook, Queen or Pawn is present, Checkmate still possible
                    if piece.__class__.__name__ in ["Rook", "Queen", "Pawn"]:
                        return False 

                    # Verify if a Knight is present
                    if piece.__class__.__name__ == "Knight":
                        has_other_piece = True

                    # Store bishops according to their square color
                    if piece.__class__.__name__ == "Bishop":
                        square_color = (piece.position[0] + piece.position[1]) % 2
                        bishops["light" if square_color == 0 else "dark"] += 1

        num_pieces = len(pieces)

        # Case 1: Only 2 kings
        if num_pieces == 2:
            print("⚖️ Draw : Insufficient material (King vs King).")
            return True

        # Case 2: King + (Knight OR Bishop) vs Single King
        if num_pieces == 3:
            for piece in pieces:
                if piece.__class__.__name__ not in ["Bishop", "Knight", "King"]:
                    return False
                else:
                    print("⚖️ Draw : Insufficient material (King vs King et Knight/Bishop)")
                    return True

        # Case 3: King and Bishop vs King and Bishop (same square's color)
        if num_pieces == 4 and sum(bishops.values()) == 2 and min(bishops.values()) == 0:
            print("⚖️ Draw : Insufficient material (King and Bishop vs King and Bishop on same square's color).")
            return True

        # Case 4: multiple Bishops but ALL on same square color and no other pieces
        if sum(bishops.values()) > 0 and min(bishops.values()) == 0 and not has_other_piece:
            print("⚖️ Draw : All remaining Bishops are on the same square's color and no other pieces can help.")
            return True

        return False
