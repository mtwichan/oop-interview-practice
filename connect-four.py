from enum import Enum
from random import random
from typing import List, Tuple
from random import randint
import time

class Symbol(Enum):
    RED = "R"
    BLACK = "B"
    EMPTY = "-"

class Player:
    COLORS = {"RED": Symbol.RED.value, "BLACK": Symbol.BLACK.value}

    def __init__(self, playerColor: str):
        self.__color: str = playerColor

    @property
    def color(self) -> str:
        return self.__color

    @property
    def symbol(self) -> str:
        return self.COLORS[self.__color]

class AIPlayer(Player):
    def __init__(self, playerColor: str):
        super().__init__(playerColor)
    
    def playerInput(self, columnSize: int):
        time.sleep(1)
        randomColumn: int = randint(0, columnSize - 1)
        print(f"Player AI selected column at {randomColumn}")
        return randomColumn

class ConnectFour:
    def __init__(self, rowSize: int, columnSize: int, AIEnabled=False):
        if not isinstance(rowSize, int) or not isinstance(columnSize, int):
            raise TypeError()

        if rowSize < 4 or columnSize < 4:
            raise ValueError("Board must be greater or equal to 4 x 4")
        
        self.boardRowSize: int = rowSize
        self.boardColSize: int = columnSize
        self.boardSize: int = rowSize * columnSize

        self.__AIEnabled: bool = AIEnabled
        self.__playerRed: Player =  AIPlayer("RED") if AIEnabled else Player("RED")
        self.__playerBlack: Player = Player("BLACK")
        self.__board: List[List] = self.__createBoard(rowSize, columnSize)
        self.__boardColFull: List = [False for _ in range(self.boardColSize)]
        
    def play(self):
        isGameRunning: bool = True
        turns: int = 1
        selectedRow: int = -1
        selectedColumn: int = -1
        selectedPlayer: str = None

        print("Game starting ...")
        while isGameRunning:

            if turns % 2 == 1:
                blackColumn = self.__playerInput(self.__playerBlack.color)
                selectedPlayer = self.__playerBlack.symbol
                selectedPlayerName = self.__playerBlack.color
                selectedRow, selectedColumn = self.__playerMove(
                    selectedPlayer, blackColumn
                )
            else:
                redColumn = self.__playerRed.playerInput(self.boardColSize) if self.__AIEnabled else self.__playerInput(self.__playerRed.color)
                selectedPlayer = self.__playerRed.symbol
                selectedPlayerName = self.__playerRed.color
                selectedRow, selectedColumn = self.__playerMove(
                    selectedPlayer, redColumn
                )

            self.printBoard()

            if self.__isWin(selectedRow, selectedColumn, selectedPlayer):
                isGameRunning: bool = False
                print(f"Game Over: Player {selectedPlayerName} wins!")
            elif turns == self.boardSize:
                isGameRunning = False
                print(print(f"Game Over: Tie game. No more moves remaining."))

            turns += 1

        print("Game over! Thanks for playing :)")

    def printBoard(self) -> None:
        header = str([f"{col}" for col in range(self.boardColSize)]).replace(
            ",", " "
        )
        header = header.replace("'", " ")
        print(header)

        for row in self.__board:
            rowToPrint = str(row).replace(",", " ")
            rowToPrint = rowToPrint.replace("'", " ")
            print(rowToPrint)
        print("\n")

    def __playerInput(self, playerColor: str) -> int:
        selectedColumn: int = None
        while True:
            try:
                selectedColumn = int(input(f"Player {playerColor} select a column: "))
                if selectedColumn > self.boardColSize or selectedColumn < 0:
                    raise ValueError("Selected column is out of bounds")

                if self.__boardColFull[selectedColumn]:
                    raise Exception("Column is full select another column")
                break
            except Exception as e:
                print(e)
        return selectedColumn

    def __playerMove(self, playerSymbol: str, selectedColumn: int) -> Tuple:
        for rowIdx in range(self.boardRowSize - 1, -1, -1):
            cell = self.__board[rowIdx][selectedColumn]
            if cell == "-":
                self.__board[rowIdx][selectedColumn] = playerSymbol

                if rowIdx == 0:
                    self.__boardColFull[selectedColumn] = True
                return rowIdx, selectedColumn
                break

    def __createBoard(self, rowSize: int, columnSize: int) -> List[List]:
        board: List[List] = [
            [Symbol.EMPTY.value] * columnSize for _ in range(rowSize)
        ]
        return board

    def __str__(self) -> str:
        return self.__board

    def __isVerticalWin(self, column: int, playerSymbol: str) -> bool:
        count: int = 0
        for row in self.__board:
            cell = row[column]

            if cell == playerSymbol:
                count += 1
            else:
                count = 0

            if count == 4:
                return True

        return False

    def __isHorizontalWin(self, row: int, playerSymbol: str) -> bool:
        count: int = 0
        for cell in self.__board[row]:
            if count == 4:
                return True

            if cell == playerSymbol:
                count += 1
            else:
                count = 0

        return False

    def __isDiagonalWinPos(self, player: str) -> bool:
        for colIdx in range(self.boardColSize - 3):
            for rowIdx in range(self.boardRowSize - 3):
                if (
                    self.__board[rowIdx][colIdx] == player
                    and self.__board[rowIdx + 1][colIdx + 1] == player
                    and self.__board[rowIdx + 2][colIdx + 2] == player
                    and self.__board[rowIdx + 3][colIdx + 3] == player
                ):
                    return True
        return False

    def __isDiagonalWinNeg(self, player: str) -> bool:
        for colIdx in range(self.boardColSize - 3):
            for rowIdx in range(3, self.boardRowSize):
                if (
                    self.__board[rowIdx][colIdx] == player
                    and self.__board[rowIdx - 1][colIdx + 1] == player
                    and self.__board[rowIdx - 2][colIdx + 2] == player
                    and self.__board[rowIdx - 3][colIdx + 3] == player
                ):
                    return True
        return False

    def __isWin(self, row: int, column: int, player: str):
        return (
            self.__isHorizontalWin(row, player)
            or self.__isDiagonalWinNeg(player)
            or self.__isDiagonalWinPos(player)
            or self.__isVerticalWin(column, player)
        )


def main():
    game = ConnectFour(10, 10, AIEnabled=True)
    game.play()

main()