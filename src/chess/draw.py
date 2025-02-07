import pygame
from window import window as w
from chess import globals as g
from chess import util
from sprites import sprites as s


def getPieceName(pieceVal):
    name = ""

    piece: g.Piece = g.Piece()

    colour = lambda val: "black" if val == 16 else "white"
    pieces = {
        piece.King: "King",
        piece.Pawn: "Pawn",
        piece.Knight: "Knight",
        piece.Bishop: "Bishop",
        piece.Rook: "Rook",
        piece.Queen: "Queen",
    }

    name = colour(pieceVal & 0b11000) + pieces[pieceVal & 0b00111] + ".png"

    return name


def drawPieces(window: w.PygameWindow):

    sSheet = s.SpriteSheet("assets/piece_sprites.png")
    sprite = None

    for i in range(len(g.board)):
        if g.board[i] != 0:
            sprite = pygame.transform.scale(
                sSheet.GetSprite(getPieceName(g.board[i]), 256, 256), (g.side, g.side)
            )

            window.screen.blit(
                sprite,
                (
                    g.squareCentres[i][0] - (g.side / 2),
                    g.squareCentres[i][1] - (g.side / 2),
                ),
            )


isInit = False


def drawBoard(window: w.PygameWindow):

    window.screen.fill((49, 46, 43))

    white: tuple = (240, 218, 181)
    black: tuple = (181, 135, 99)

    g.size = pygame.display.get_surface().get_size()

    # Math!
    offset: float = (g.size[1] - (g.weight * g.size[1])) / 2
    size: float = pygame.display.get_surface().get_size()
    boardSize: float = g.size[1] * g.weight

    g.boardSize = boardSize

    side: int = boardSize / 8
    g.side = side
    startPos: tuple = ((g.size[0] - boardSize) / 2, offset)

    calculateCentres = lambda squarePos, side: (
        squarePos[0] + (side / 2),
        squarePos[1] + (side / 2),
    )

    row: int = 0

    colour = lambda x: white if (x % 2) else black

    # find the centres of the squares
    g.boardImage = pygame.transform.scale(g.imageCopy, (boardSize, boardSize))
    while row < 8:

        column: int = 0

        while column < 8:

            g.squareCentres[util.coordsToIndex(7 - row, column)] = calculateCentres(
                (startPos[0] + (column * side), offset + (row * side)), side
            )
            column += 1
        row += 1

    # draw board
    window.screen.blit(g.boardImage, startPos)
    g.prevSize = size

    isInit = True
