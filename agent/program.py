from referee.game import PlayerColor, Coord, Direction, \
    Action, MoveAction, GrowAction
from .agent_board import AgentBoard
from copy import deepcopy
from collections import deque

class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        # Initialize the agent with its color and the opponent's color
        self._color = color
        self._opponent = color.opponent
        from referee.game.board import Board
        # Create an AgentBoard using the current board state
        self._board = AgentBoard(Board()._state)
        print(f"[INIT] I am playing as {self._color}")

    def action(self, **referee: dict) -> Action:
        board_copy = self._board.copy()
        # Run minimax to determine the best move
        best_score, best_action = self.minimax(
            board_copy, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing=True
        )

        # Return the selected action, fallback to GrowAction if no move found
        return best_action or GrowAction()

    def update(self, color: PlayerColor, action: Action, **referee: dict):
        # Update internal board state based on the actual move
        self._board.apply_action(action, color)
        print(f"[UPDATE] {color} performed {action}")

    def minimax(self, board: AgentBoard, depth: int, alpha: float, beta: float, maximizing: bool) -> tuple[int, Action | None]:
        # Base case: if depth is 0, return the evaluation of the board
        if depth == 0:
            return self.evaluate(board), None

        current_color = self._color if maximizing else self._opponent
        actions = self.get_all_actions(board, current_color)

        best_action = None
        if maximizing:
            max_eval = float('-inf')
            for action in actions:
                # Simulate action
                new_board = board.copy()
                new_board.apply_action(action, current_color)
                # Recursively evaluate
                eval_score, i = self.minimax(new_board, depth - 1, alpha, beta, False)
                # Track best action
                if eval_score > max_eval:
                    max_eval, best_action = eval_score, action
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Alpha-beta pruning
            return max_eval, best_action
        else:
            min_eval = float('inf')
            for action in actions:
                new_board = board.copy()
                new_board.apply_action(action, current_color)
                eval_score, i = self.minimax(new_board, depth - 1, alpha, beta, True)
                if eval_score < min_eval:
                    min_eval, best_action = eval_score, action
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha-beta pruning
            return min_eval, best_action

    def get_all_actions(self, board: AgentBoard, color: PlayerColor) -> list[Action]:
        actions = []

        # Iterate over all frogs of the player
        for frog in board.get_frogs(color):
            if board.is_goal_row(frog, color):
                continue  # Skip frogs that reached the goal

            visited = set()
            queue = deque([(frog, [])])
            visited.add(frog)

            # BFS to generate all possible multi-jump actions
            while queue:
                pos, path = queue.popleft()
                for d in board.allowed_directions(color):
                    mid = board.safe_add(pos, d)
                    end = board.safe_add(pos, d, 2)
                    if (
                        mid and end and
                        board.is_valid_jump(mid, end) and
                        end not in visited
                    ):
                        new_path = path + [d]
                        actions.append(MoveAction(frog, new_path))
                        queue.append((end, new_path))
                        visited.add(end)

            # Add valid step actions if not part of a valid jump
            for d in board.allowed_directions(color):
                step = board.safe_add(frog, d)
                mid = board.safe_add(frog, d)
                end = board.safe_add(frog, d, 2)

                if step and board.is_valid_step(step):
                    if not (mid and end and board.is_valid_jump(mid, end)):
                        actions.append(MoveAction(frog, [d]))

        # Helper function to check forward direction for the given player
        def is_forward(d: Direction, color: PlayerColor) -> bool:
            return d in {
                PlayerColor.RED: {Direction.Down, Direction.DownLeft, Direction.DownRight},
                PlayerColor.BLUE: {Direction.Up, Direction.UpLeft, Direction.UpRight}
            }[color]

        # Sort actions to prefer forward progress over GrowActions 
        actions.sort(key=lambda act: (
            1 if isinstance(act, GrowAction) else
            -sum(1 for d in act.directions if is_forward(d, color))
        ))

        # Only return Grow if no MoveActions are possible
        return actions if actions else [GrowAction()]

    def evaluate(self, board: AgentBoard) -> int:
        score = 0
        # Evaluate board state based on frog positions
        for coord, cell in board.state.items():
            if cell.state == self._color:
                # Reward based on progress and goals
                row_progress = coord.r if self._color == PlayerColor.RED else (7 - coord.r)
                score += 20
                score += row_progress * 10

                if row_progress >= 4:
                    score += 15  # Bonus for advancing beyond mid-board

                if board.is_goal_row(coord, self._color):
                    score += 100  # Big bonus for reaching the goal

                # Penalize if stuck near starting side
                if self._color == PlayerColor.RED and coord.r <= 2:
                    score -= 10
                if self._color == PlayerColor.BLUE and coord.r >= 5:
                    score -= 10

            elif cell.state == self._opponent:
                # Penalize opponent progress
                row_progress = coord.r if self._opponent == PlayerColor.RED else (7 - coord.r)
                score -= 20
                score -= row_progress * 10
                if board.is_goal_row(coord, self._opponent):
                    score -= 100

        return score


