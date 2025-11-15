"""Game logic for Tic Tac Toe."""

from enum import Enum
from typing import Optional


class Player(Enum):
    """Represents a player in the game."""
    X = "X"
    O = "O"


class GameState(Enum):
    """Represents the current state of the game."""
    PLAYING = "playing"
    X_WON = "x_won"
    O_WON = "o_won"
    DRAW = "draw"


class TicTacToe:
    """Main game logic for Tic Tac Toe."""

    def __init__(self):
        """Initialize a new game."""
        self.board: list[Optional[Player]] = [None] * 9
        self.current_player = Player.X
        self.state = GameState.PLAYING

    def make_move(self, position: int) -> bool:
        """
        Make a move at the specified position.

        Args:
            position: Board position (0-8)

        Returns:
            True if move was successful, False otherwise
        """
        if self.state != GameState.PLAYING:
            return False

        if position < 0 or position > 8:
            return False

        if self.board[position] is not None:
            return False

        self.board[position] = self.current_player
        self._check_game_state()

        if self.state == GameState.PLAYING:
            self.current_player = Player.O if self.current_player == Player.X else Player.X

        return True

    def _check_game_state(self) -> None:
        """Check if the game has been won or drawn."""
        # Check rows
        for i in range(0, 9, 3):
            if (self.board[i] is not None and
                self.board[i] == self.board[i + 1] == self.board[i + 2]):
                self.state = (GameState.X_WON if self.board[i] == Player.X 
                             else GameState.O_WON)
                return

        # Check columns
        for i in range(3):
            if (self.board[i] is not None and
                self.board[i] == self.board[i + 3] == self.board[i + 6]):
                self.state = (GameState.X_WON if self.board[i] == Player.X 
                             else GameState.O_WON)
                return

        # Check diagonals
        if (self.board[0] is not None and
            self.board[0] == self.board[4] == self.board[8]):
            self.state = (GameState.X_WON if self.board[0] == Player.X 
                         else GameState.O_WON)
            return

        if (self.board[2] is not None and
            self.board[2] == self.board[4] == self.board[6]):
            self.state = (GameState.X_WON if self.board[2] == Player.X 
                         else GameState.O_WON)
            return

        # Check for draw
        if all(cell is not None for cell in self.board):
            self.state = GameState.DRAW

    def reset(self) -> None:
        """Reset the game to initial state."""
        self.board = [None] * 9
        self.current_player = Player.X
        self.state = GameState.PLAYING

    def get_winner(self) -> Optional[Player]:
        """Get the winning player if any."""
        if self.state == GameState.X_WON:
            return Player.X
        elif self.state == GameState.O_WON:
            return Player.O
        return None
