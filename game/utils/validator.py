from abc import ABC
from typing import List
from core.tile import Tile
from core.worker import Worker
from core.board import Board
from core.position import Position

class Validator(ABC):
    """Provides static validation methods to determine valid moves and builds for a worker on the Santorini game board."""

    @staticmethod
    def get_valid_move_tiles(worker: Worker, board: Board) -> List[Tile]:
        """
        Returns a list of tiles that the given worker can legally move to.

        Movement rules:
            1. Must move to an adjacent tile (including diagonals).
            2. The destination tile must not contain another worker.
            3. The destination tile must not have a dome.
            4. The worker can move up at most one level higher than its current tile's building height.

        """
        valid: List[Tile] = []
        cur_tile = board.get_tile(worker.position)
        cur_level = cur_tile.building.level if cur_tile.building else 0

        for x in range(board.width):
            for y in range(board.height):
                tile = board.get_tile(Position(x, y))

                # 1. Must be adjacent (including diagonals)
                dx = abs(x - worker.position.x)
                dy = abs(y - worker.position.y)
                if max(dx, dy) != 1:
                    continue

                # 2. Tile must be empty of other workers
                if tile.has_worker():
                    continue

                # 3. Cannot move onto a dome
                if tile.building and tile.building.has_dome():
                    continue

                # 4. Can only move up at most one level
                tgt_level = tile.building.level if tile.building else 0
                if tgt_level - cur_level > 1:
                    continue

                valid.append(tile)

        return valid

    @staticmethod
    def get_valid_build_tiles(worker: Worker, board: Board) -> List[Tile]:
        """
        Returns a list of tiles where the given worker can legally build.

        Building rules:
            1. Must build on an adjacent tile (including diagonals).
            2. Cannot build where a worker is present.
            3. Cannot build on a dome or a completed tower.

        """
        valid: List[Tile] = []
        wp = worker.position

        for x in range(board.width):
            for y in range(board.height):
                tile = board.get_tile(Position(x, y))

                # 1. Must be adjacent
                dx = abs(x - wp.x)
                dy = abs(y - wp.y)
                if max(dx, dy) != 1:
                    continue

                # 2. Cannot build where there's a worker
                if tile.has_worker():
                    continue

                # 3. Cannot build on a dome
                if tile.building and tile.building.has_dome():
                    continue

                valid.append(tile)

        return valid
