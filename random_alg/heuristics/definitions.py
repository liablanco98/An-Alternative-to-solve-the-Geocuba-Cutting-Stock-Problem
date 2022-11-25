

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


class Sub_Sheet:
    def __init__(self, length: int, width: int,  space: int = 0) -> None:
        self.space: int = space
        self.left_length: int = length
        self.left_width: int = width
        self.current_length_pos: int = 0
        self.current_width_pos: int = 0
        self.items: list[tuple[int, int, Piece]] = []

    def __repr__(self) -> str:
        '''
            Represents the class as a string
        '''
        return f'Pos:({self.current_length_pos},{self.current_width_pos})- Left({self.left_length},{self.left_width})\n'

    def __eq__(self, other: object) -> bool:
        '''
            Return if is equal to other sub_sheet
        '''
        return isinstance(other, Sub_Sheet) and self.current_length_pos == other.current_length_pos and self.current_width_pos == other.current_width_pos

    def increase_length(self, to_add: int) -> None:
        self.left_length += to_add

    def increase_width(self, to_add: int) -> None:
        self.left_width += to_add

    def fit_piece_rigth(self, piece: Piece) -> bool:
        '''
            Returns if a Piece can be Colocate at right
        '''
        return piece.length+self.space <= self.left_length

    def fit_piece_bottom(self, piece: Piece) -> bool:
        '''
            Returns if a Piece can be Colocate at the buttom
        '''
        return piece.width+self.space <= self.left_width

    def colocate_rigth_piece(self, piece: Piece):
        '''
            Colocate a piece to the rigth of the current piece
        '''
        new_piece_located = (self.current_length_pos,
                             self.current_length_pos+piece.length, piece)
        self.items.append(new_piece_located)

        self.left_length -= piece.length+self.space
        self.current_length_pos += piece.length+self.space
        self.current_width_pos = max(self.current_width_pos, piece.width)

    def colocate_bottom_piece(self, piece: Piece):
        '''
            Colocate a piece at the bottom of the current piece
        '''
        new_piece_located = (self.current_width_pos,
                             self.current_width_pos+piece.width, piece)
        self.items.append(new_piece_located)

        self.left_width -= piece.width+self.space
        self.current_width_pos += piece.width+self.space
        self.current_length_pos = max(self.current_length_pos, piece.length)


class Subject:
    '''
    A subject has:
        - The stock
        - The pieces placed
        - The heuristic number and the method it uses
        - The resulting pattern of placing pieces with that heuristic
        - The residue pattern
        - An array with 0 in pos representing a piece that is not used in the pattern, otherwise the number of times the piece appears
    '''

    def __init__(self, stock: Stock, dic: dict, pieces: list[Piece], heuristic_number: int, heuristic,b:bool=False) -> None:
        self.pieces: list[Piece] = pieces
        self.heuristic_number: int = heuristic_number
        self.heuristic = heuristic

        self.waste, self.pattern, self.pieces_used = self.heuristic(
            stock, self.pieces,b)
        self.pieces: list[Piece] = list(map(lambda x: x[2],self.pattern))
        self.all_pieces_considered: list[int] = self.pieces_dic(
            stock=stock, dic=dic)

    def __repr__(self) -> str:
        '''
            Represents the class as a string
        '''
        return f'Desperdicio:{self.waste} - Heuristica: {self.heuristic_number}\n Piezas:{self.pieces_used}\n'

    def __eq__(self, other: object) -> bool:
        '''
            Return if is equal to other subjetc
        '''
        return isinstance(other, Subject) and self.pattern == other.pattern

    def pieces_dic(self, stock: Stock, dic: dict) -> list[int]:
        '''
        parameters:
            - the stock
            - a dictionary where key=pieces id and value=pieces position
        Return:
            - An array with 0 in pos representing a piece that is not used in the pattern, otherwise the number of times the piece appears
        '''

        all_pieces_considered = [0]*len(stock.pieces)
        for p, d in self.pieces_used.items():
            pos = dic[p.id]
            all_pieces_considered[pos] = d
        return all_pieces_considered
