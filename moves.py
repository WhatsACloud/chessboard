from movesClass import Move, Direction

Bishop = Moves()
Bishop.add(
    Move([Direction.up, Direction.left]),
    Move([Direction.left, Direction.down]),
    Move([Direction.down, Direction.right]),
    Move([Direction.right, Direction.up]),
)

Rook = Moves()
Rook.add(
    Move([Direction.up]),
    Move([Direction.down]),
    Move([Direction.left]),
    Move([Direction.right]),
)

Horse = Moves()
Horse.add(
    Move([Direction.up * 3, Direction.left], 1),
    Move([Direction.up * 3, Direction.right], 1),
    Move([Direction.left * 3, Direction.up], 1),
    Move([Direction.left * 3, Direction.down], 1),
    Move([Direction.down * 3, Direction.left], 1),
    Move([Direction.down * 3, Direction.right], 1),
    Move([Direction.right * 3, Direction.up], 1),
    Move([Direction.right * 3, Direction.down], 1),
)

Queen = Moves()
Queen.add(
    Move([Direction.up]),
    Move([Direction.down]),
    Move([Direction.left]),
    Move([Direction.right]),
    Move([Direction.up, Direction.left]),
    Move([Direction.left, Direction.down]),
    Move([Direction.down, Direction.right]),
    Move([Direction.right, Direction.up]),
)

King = Moves()
King.add(
    Move([Direction.up], 1),
    Move([Direction.down], 1),
    Move([Direction.left], 1),
    Move([Direction.right], 1),
    Move([Direction.up, Direction.left], 1),
    Move([Direction.left, Direction.down], 1),
    Move([Direction.down, Direction.right], 1),
    Move([Direction.right, Direction.up], 1),
)
