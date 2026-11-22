from referee.game import Coord, Direction, PlayerColor, Action
from referee.game.board import CellState
from referee.game.actions import MoveAction, GrowAction
from copy import deepcopy

BOARD_SIZE = 8  # Freckers board size

class AgentBoard:
    def __init__(self, initial_board: dict[Coord, CellState]):
        # Make a deep copy so we can safely change our own internal board state
        self.state: dict[Coord, CellState] = deepcopy(initial_board)

    def copy(self):
        # Return a deep copy of the board (used in Minimax to simulate moves)
        return AgentBoard(self.state)

    def get_frogs(self, color: PlayerColor) -> list[Coord]:
        # Return coordinates of all frogs of a specific color
        return [coord for coord, cell in self.state.items() if cell.state == color]

    def allowed_directions(self, color: PlayerColor):
        # Return list of directions a player can move in
        if color == PlayerColor.RED:
            return [Direction.Right, Direction.Left,
                    Direction.Down, Direction.DownLeft, Direction.DownRight]
        else:
            return [Direction.Right, Direction.Left,
                    Direction.Up, Direction.UpLeft, Direction.UpRight]

    def safe_add(self, coord: Coord, d: Direction, times: int = 1):
        # Safely compute a new coordinate by moving in direction `d`, `times` times
        r = coord.r + d.r * times
        c = coord.c + d.c * times
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            return Coord(r, c)
        return None  # Out of bounds

    def is_valid_step(self, dest: Coord) -> bool:
        # Check if the destination is a lily pad
        return self.state[dest].state == "LilyPad"

    def is_valid_jump(self, mid: Coord, end: Coord) -> bool:
        # Check if we can jump: mid must have a frog, and end must be a lily pad
        return (self.state[mid].state in (PlayerColor.RED, PlayerColor.BLUE)
                and self.state[end].state == "LilyPad")

    def apply_move(self, move: MoveAction, color: PlayerColor):
        # Apply a MoveAction for a frog of given color
        pos = move.coord  # Starting position of the frog
        if self.state[pos].state != color:
            raise ValueError(f"no {color} frog at {pos}")
        
        # Remove frog from its starting position (mark it empty)
        self.state[pos] = CellState(None)

        # Traverse the path of directions in the move
        for d in move.directions:
            step = self.safe_add(pos, d)      
            jump = self.safe_add(pos, d, 2)   
            if jump and step and self.is_valid_jump(step, jump):
                pos = jump  
            elif step and self.is_valid_step(step):
                pos = step  
            else:
                raise ValueError(f"illegal move from {move.coord} via {move.directions}")

        # Place frog at final destination
        self.state[pos] = CellState(color)

    def apply_grow(self, color: PlayerColor):
        # Apply a GrowAction for the given color
        new_pads = []
        for frog in self.get_frogs(color):
            # Look in all 8 directions
            for d in Direction:
                nbr = self.safe_add(frog, d)
                # If the neighbor is empty, mark it for lily pad growth
                if nbr and self.state[nbr].state is None:
                    new_pads.append(nbr)

        # Place lily pads in all valid adjacent empty tiles
        for nbr in new_pads:
            self.state[nbr] = CellState("LilyPad")

    def apply_action(self, action: Action, color: PlayerColor):
        # Apply either MoveAction or GrowAction
        if isinstance(action, MoveAction):
            self.apply_move(action, color)
        elif isinstance(action, GrowAction):
            self.apply_grow(color)
        else:
            raise ValueError(f"Unknown action {action}")

    def is_goal_row(self, coord: Coord, color: PlayerColor) -> bool:
        # Check if a coordinate is in the goal row for a given color
        return (color == PlayerColor.RED and coord.r == BOARD_SIZE-1) or \
               (color == PlayerColor.BLUE and coord.r == 0)


   # This is a helper function which was used to print the board
   # def __str__(self):
        
    #    sym = {
    #        None: ".",                
    #        "LilyPad": "◦",          
    #        PlayerColor.RED: "R",   
    #        PlayerColor.BLUE: "B"    
    #    }
    #    rows = []
    #    for r in range(BOARD_SIZE):
    #        row = []
    #        for c in range(BOARD_SIZE):
    #            row.append(sym[self.state[Coord(r, c)].state])
    #        rows.append(f"{r} " + " ".join(row))
    #    return "\n".join(rows)

