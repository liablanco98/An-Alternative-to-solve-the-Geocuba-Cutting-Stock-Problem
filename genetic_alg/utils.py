from .heuristics.definitions import Piece, Stock


def get_rotated(stock: Stock) -> list[tuple[Piece, int]]:
    '''
        Build for each piece a new piece inverted
        Parameters:
            - stock : A stock
        Return:
            -List [p,i]:  p is a piece inverted, i is the demand of that piece originally
    '''
    solution: list[tuple[Piece, int]] = []
    for piece, demand in stock.pieces:
        if piece.length+stock.space > stock.width or piece.width+stock.space > stock.length:
            continue
        rotated = Piece(id=piece.id, length=piece.width,
                        width=piece.length, incompatible=piece.incompatible)
        rotated.rotate()
        solution.append((rotated, demand))
    return solution


def valid_stock_pieces(stock: Stock) -> list[tuple[Piece, int]]:
    '''
        Is to ensure that all stock pieces width <= stock 
        width and pieces length <= stock length
        Parameters:
            - stock : A stock
        Return:
            -List [p,i]:  p is a piece valid and i the demand    
    '''
    stock_pieces: list[tuple[Piece, int]] = []
    for piece, demand in stock.pieces:
        if piece.length+stock.space > stock.length or piece.width+stock.space > stock.width:
            continue
        stock_pieces.append((piece, demand))
    return stock_pieces


def get_diferent_pieces(stock: Stock) -> list[tuple[Piece, int]]:
    rotated = get_rotated(stock)
    no_rotated = valid_stock_pieces(stock)
    return rotated+no_rotated


def extend_pieces(all_pieces: list[tuple[Piece, int]]):
    '''
        For each piece of stock pieces and that pieces rotated,
        exted it the number of times that is need it
        Parameters:
            -list[(Pieces,int)]
        Return:
            -list[Piece]
    '''
    new_pieces: list[Piece] = []
    for piece, demand in all_pieces:
        ext = [piece]*demand
        new_pieces.extend(ext)
    return new_pieces


def get_max_pieces_number(stock: Stock):
    '''
        Calculate the max number of pieces possible in one pattern.
        It will define the size of the pieces array
        Parameters:
            -stock
        Return:
            -int that represents the max number of pieces possible in one pattern
    '''
    m = min(stock.pieces, key=lambda x: x[0].area())
    max_times_possible = int(stock.area()/m[0].area())
    return max_times_possible


def hash_pieces_list(pieces_len: int, heuristic_number: int, pieces_list: list[Piece]) -> int:
    text = str(heuristic_number)

    for piece in pieces_list:
        dif = pieces_len-len(str(piece.id))
        text = text+'0'*dif+str(piece.id)
        if piece.rotation:
            text = text+str(1)
        else:
            text = text+str(0)

    return hash(text)
