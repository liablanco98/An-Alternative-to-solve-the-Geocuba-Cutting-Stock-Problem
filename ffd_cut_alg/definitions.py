

class Piece:
    '''
    One piece has:
        - identifier (id)
        - length
        - width
        - a set of colors
    '''

    def __init__(self, id: int, length: int, width: int, incompatible: set[int]):
        self.id: int = id
        self.length: int = length
        self.width: int = width
        self.incompatible: set[int] = incompatible
        self.rotation: bool = False

    def __hash__(self) -> int:
        return self.id

    def __repr__(self) -> str:
        '''
            Represents the class as a string
        '''
        return f"Pieza {self.id} ({self.length},{self.width})"

    def __eq__(self, other_piece: object) -> bool:
        '''
            Return if is equal to other_piece
        '''
        return isinstance(other_piece, Piece) and self.id == other_piece.id

    def rotate(self) -> None:
        '''
            Rotate the piece
        '''
        self.rotation = not self.rotation

    def area(self) -> int:
        '''
            Calculate the area of the piece
        '''
        return self.length*self.width

    def area_with_space(self, space: int) -> int:
        '''
            Calculate the area of the piece when a space is needed
        '''
        return (self.length+space)*(self.width+space)


class Stock:
    '''
    One stock has:
        - length
        - width
        - pieces : (Piece,times)
        - space
    '''

    def __init__(self, length: int = 700, width: int = 500, pieces: list[tuple[Piece, int]] = [], space: int = 0):
        self.length: int = length
        self.width: int = width
        self.check_pieces(pieces)
        self.pieces: list[tuple[Piece, int]] = pieces
        self.space: int = space
        self.stock_area: int = self.area()
        self.pieces_area: list[int] = self.all_pieces_area()
        self.demand_list: list[int] = [demand for _, demand in pieces]
        self.neg_demand_list: list[int] = [-demand for _, demand in pieces]

    def __repr__(self) -> str:
        '''
            Represents the class as a string
        '''
        return f"Stock largo:{self.length}, alto:{self.width}\n{self.pieces}\n"

    def check_pieces(self, to_check: list[tuple[Piece, int]]) -> None | Exception:
        '''
            This method verifies that each piece can be placed on a sheet
        '''
        for piece, _ in to_check:
            if (piece.length > self.length and piece.length > self.width) or (piece.width > self.length and piece.width > self.width):
                raise Exception(
                    f"Existe la pieza {piece} con dimensiones incorrectas")

    def area(self):
        '''
            Calculate the area of the sheets
        '''
        return self.length*self.width

    def all_pieces_area(self):
        l: list[int] = [piece.area_with_space(
            self.space) for piece, _ in self.pieces]
        return l
