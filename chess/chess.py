import pygame
import os
import sys
import win32com.client
import random

def create_or_update_shortcut(window_title, icon_path):
    try:
        # Get the absolute path of the script
        script_path = os.path.abspath(__file__)

        # Specify Python executable (use pythonw.exe explicitly)
        pythonw_exe = r'C:\Users\YourUsername\AppData\Local\Programs\Python\Python3.12.4\pythonw.exe'

        # Create shortcut path
        shortcut_path = os.path.join(os.path.expanduser('~'), 'Desktop', f'{window_title}.lnk')

        # Initialize Shell object
        shell = win32com.client.Dispatch("WScript.Shell")

        # Check if the shortcut already exists
        if os.path.exists(shortcut_path):
            # Get existing shortcut
            shortcut = shell.CreateShortcut(shortcut_path)

            # Check if existing shortcut needs update
            if (shortcut.TargetPath.lower() != pythonw_exe.lower() or 
                shortcut.Arguments.lower() != f'"{script_path}"' or 
                shortcut.IconLocation.lower() != icon_path.lower()):
                # Update the shortcut properties
                shortcut.TargetPath = pythonw_exe
                shortcut.Arguments = f'"{script_path}"'
                shortcut.IconLocation = icon_path
                shortcut.Save()
                print(f"Shortcut updated: {shortcut_path}")
            else:
                print(f"Shortcut already up-to-date: {shortcut_path}")
        else:
            # Create new shortcut
            shortcut = shell.CreateShortcut(shortcut_path)
            shortcut.TargetPath = pythonw_exe
            shortcut.Arguments = f'"{script_path}"'
            shortcut.IconLocation = icon_path
            shortcut.Save()
            print(f"Shortcut created with icon: {shortcut_path}")

    except Exception as e:
        print(f"Error creating or updating shortcut: {e}")

# Initialize Pygame
pygame.init()

# Set window title and icon path
window_title = "Chess"
icon_path = r"C:\python\chess\icon.ico"  # Replace with the path to your .ico file
script_to_run = os.path.abspath(__file__)

# Create or update the shortcut with the icon
create_or_update_shortcut(window_title, icon_path)

# Window size
window_size = (850, 850)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Chess")

# Load images
chessboard = pygame.image.load('C:\\python\\chess\\chessboard.png')
whitepawn = pygame.image.load('C:\\python\\chess\\whitepawn.png')
whiterook = pygame.image.load('C:\\python\\chess\\whiterook.png')
whitebishop = pygame.image.load('C:\\python\\chess\\whitebishop.png')
whiteknight = pygame.image.load('C:\\python\\chess\\whiteknight.png')
whitequeen = pygame.image.load('C:\\python\\chess\\whitequeen.png')
whiteking = pygame.image.load('C:\\python\\chess\\whiteking.png')
blackpawn = pygame.image.load('C:\\python\\chess\\blackpawn.png')
blackrook = pygame.image.load('C:\\python\\chess\\blackrook.png')
blackbishop = pygame.image.load('C:\\python\\chess\\blackbishop.png')
blackknight = pygame.image.load('C:\\python\\chess\\blackknight.png')
blackqueen = pygame.image.load('C:\\python\\chess\\blackqueen.png')
blackking = pygame.image.load('C:\\python\\chess\\blackking.png')
circle = pygame.image.load("C:\\python\\chess\\circle.png")
icon = pygame.image.load('C:\\python\\chess\\icon.ico')

# Set icon for window
pygame.display.set_icon(icon)

# Fill the screen with white (optional)
screen.fill((255, 255, 255))

# Function to blit all pieces to the screen
def blit_pieces(available_moves=None):
    global choose
    # Blit the chessboard
    screen.blit(chessboard, (0, 0))
    
    # Blit promotion choices
    if flag:
        choose = True
        # Debug check for image loading
        if whiteknight:
            screen.blit(whiteknight, (223.125, 435.625))
        if whitebishop:
            screen.blit(whitebishop, (329.375, 435.625))
        if whiterook:
            screen.blit(whiterook, (435.875, 435.625))
        if whitequeen:
            screen.blit(whitequeen, (542.125, 435.625))     
    elif flag1:
        choose = True
        # Debug check for image loading
        if blackknight:
            screen.blit(blackknight, (223.125, 435.625))
        if blackbishop:
            screen.blit(blackbishop, (329.375, 435.625))
        if blackrook:
            screen.blit(blackrook, (435.875, 435.625))
        if blackqueen:
            screen.blit(blackqueen, (542.125, 435.625))
    else: choose = False  
    # Blit all pieces based on their positions and visibility
    for piece_type in piece:
        for piece_name, piece_info in piece[piece_type].items():
            if piece_info['visible']:
                piece_x, piece_y = piece_info['pos']
                # Center the piece in the square
                piece_center_x = piece_x + 53.125
                piece_center_y = piece_y + 53.125
                piece_rect = piece_info['image'].get_rect(center=(piece_center_x, piece_center_y))
                screen.blit(piece_info['image'], (piece_rect.topleft))
    
    # Blit circles for available moves
    if available_moves:
        moves, promotions, en_passant_moves = available_moves  # Unpack the available moves, promotions, and en passant moves
        for move in moves + promotions + en_passant_moves:
            # Center the circle in the square
            circle_x = move[0] + 53.125 - circle.get_width() / 2
            circle_y = move[1] + 53.125 - circle.get_height() / 2
            screen.blit(circle, (circle_x, circle_y))
    
    # Update the display
    pygame.display.flip()

castling_rights = {
    'white': {'kingside': True, 'queenside': True},
    'black': {'kingside': True, 'queenside': True}
}

def update_castling_rights(move, castling_rights):
    piece, start, end = move
    if piece == 'king':
        if start == (435.625, 754.375):  # White king move
            castling_rights['white']['kingside'] = False
            castling_rights['white']['queenside'] = False
        elif start == (435.625, 10.625):  # Black king move
            castling_rights['black']['kingside'] = False
            castling_rights['black']['queenside'] = False
    elif piece == 'rook':
        if start == (10.625, 754.375):  # White queenside rook move
            castling_rights['white']['queenside'] = False
        elif start == (754.375, 754.375):  # White kingside rook move
            castling_rights['white']['kingside'] = False
        elif start == (10.625, 10.625):  # Black queenside rook move
            castling_rights['black']['queenside'] = False
        elif start == (754.375, 10.625):  # Black kingside rook move
            castling_rights['black']['kingside'] = False
 
has_moved = {
    'white': {'king': False, 'kingside_rook': False, 'queenside_rook': False},
    'black': {'king': False, 'kingside_rook': False, 'queenside_rook': False}
}
            
# Track pieces and their positions, visibility and abilities
piece = {
    'pawn': {
        'whitepawn1': {'pos': (10.625, 648.125), 'moves': [], 'promotions': [], 'enpassant': [], 'visible': True, 'image': whitepawn, 'has_moved': False, 'color' : 0},
        'whitepawn2': {'pos': (116.875, 648.125), 'moves': [], 'promotions': [], 'enpassant': [], 'visible': True, 'image': whitepawn, 'has_moved': False, 'color' : 0},
        'whitepawn3': {'pos': (223.125, 648.125), 'moves': [], 'promotions': [], 'enpassant': [], 'visible': True, 'image': whitepawn, 'has_moved': False, 'color' : 0},
        'whitepawn4': {'pos': (329.375, 648.125), 'moves': [], 'promotions': [], 'enpassant': [], 'visible': True, 'image': whitepawn, 'has_moved': False, 'color' : 0},
        'whitepawn5': {'pos': (435.625, 648.125), 'moves': [], 'promotions': [], 'enpassant': [], 'visible': True, 'image': whitepawn, 'has_moved': False, 'color' : 0},
        'whitepawn6': {'pos': (541.875, 648.125), 'moves': [], 'promotions': [], 'enpassant': [], 'visible': True, 'image': whitepawn, 'has_moved': False, 'color' : 0},
        'whitepawn7': {'pos': (648.125, 648.125), 'moves': [], 'promotions': [], 'enpassant': [], 'visible': True, 'image': whitepawn, 'has_moved': False, 'color' : 0},
        'whitepawn8': {'pos': (754.375, 648.125), 'moves': [], 'promotions': [], 'enpassant': [], 'visible': True, 'image': whitepawn, 'has_moved': False, 'color' : 0},
        'blackpawn1': {'pos': (10.625, 116.875), 'moves': [], 'promotions': [], 'enpassant': [], 'visible': True, 'image': blackpawn, 'has_moved': False, 'color' : 1},
        'blackpawn2': {'pos': (116.875, 116.875), 'moves': [], 'promotions': [], 'enpassant': [], 'visible': True, 'image': blackpawn, 'has_moved': False, 'color' : 1},
        'blackpawn3': {'pos': (223.125, 116.875), 'moves': [], 'promotions': [], 'enpassant': [], 'visible': True, 'image': blackpawn, 'has_moved': False, 'color' : 1},
        'blackpawn4': {'pos': (329.375, 116.875), 'moves': [], 'promotions': [], 'enpassant': [], 'visible': True, 'image': blackpawn, 'has_moved': False, 'color' : 1},
        'blackpawn5': {'pos': (435.625, 116.875), 'moves': [], 'promotions': [], 'enpassant': [], 'visible': True, 'image': blackpawn, 'has_moved': False, 'color' : 1},
        'blackpawn6': {'pos': (541.875, 116.875), 'moves': [], 'promotions': [], 'enpassant': [], 'visible': True, 'image': blackpawn, 'has_moved': False, 'color' : 1},
        'blackpawn7': {'pos': (648.125, 116.875), 'moves': [], 'promotions': [], 'enpassant': [], 'visible': True, 'image': blackpawn, 'has_moved': False, 'color' : 1},
        'blackpawn8': {'pos': (754.375, 116.875), 'moves': [], 'promotions': [], 'enpassant': [], 'visible': True, 'image': blackpawn, 'has_moved': False, 'color' : 1}
    },
    'rook': {
        'whiterook1': {'pos': (10.625, 754.375), 'moves': [], 'visible': True, 'image': whiterook,'moved':False, 'color' : 0},
        'whiterook2': {'pos': (754.375, 754.375), 'moves': [], 'visible': True, 'image': whiterook,'moved':False, 'color' : 0},
        'blackrook1': {'pos': (10.625, 10.625), 'moves': [], 'visible': True, 'image': blackrook,'moved':False, 'color' : 1},
        'blackrook2': {'pos': (754.375, 10.625), 'moves': [], 'visible': True, 'image': blackrook,'moved':False, 'color' : 1}
    },
    'knight': {
        'whiteknight1': {'pos': (116.875,754.375), 'moves': [], 'visible': True, 'image': whiteknight, 'color' : 0},
        'whiteknight2': {'pos': (648.125, 754.375), 'moves': [], 'visible': True, 'image': whiteknight, 'color' : 0},
        'blackknight1': {'pos': (116.875, 10.625), 'moves': [], 'visible': True, 'image': blackknight, 'color' : 1},
        'blackknight2': {'pos': (648.125, 10.625), 'moves': [], 'visible': True, 'image': blackknight, 'color' : 1}
    },
    'bishop': {
        'whitebishop1': {'pos': (223.125, 754.375), 'moves': [], 'visible': True, 'image': whitebishop, 'color' : 0},
        'whitebishop2': {'pos': (541.875, 754.375), 'moves': [], 'visible': True, 'image': whitebishop, 'color' : 0},
        'blackbishop1': {'pos': (223.125, 10.625), 'moves': [], 'visible': True, 'image': blackbishop, 'color' : 1},
        'blackbishop2': {'pos': (541.875, 10.625), 'moves': [], 'visible': True, 'image': blackbishop, 'color' : 1}
    },
    'queen': {
        'whitequeen': {'pos': (329.375, 754.375), 'moves': [], 'visible': True, 'image': whitequeen, 'color' : 0},
        'blackqueen': {'pos': (329.375, 10.625), 'moves': [], 'visible': True, 'image': blackqueen, 'color' : 1}
    },
    'king': {
        'whiteking': {'pos': (435.625, 754.375), 'moves': [], 'visible': True, 'image': whiteking,'moved':False, 'color' : 0},
        'blackking': {'pos': (435.625, 10.625), 'moves': [], 'visible': True, 'image': blackking,'moved':False, 'color' : 1}
    }
}
    
def remove_piece_at_position(position):
    """
    Remove the piece at the given position by setting its visibility to False.

    :param position: Tuple representing the position (x, y) of the piece to be removed.
    """
    # print(position)
    
    for piece_type in piece:
        for piece_name, piece_info in piece[piece_type].items():
            if piece_info['pos'] == position and piece_info['visible']:
                piece_info['visible'] = False
                return  # Exit after finding and hiding the piece

# Function to get pawn moves
def get_pawn_moves(pawn_name, pawn_info, last_move):
    moves = []
    promotions = []
    en_passant_moves = []
    x, y = pawn_info['pos']
    direction = -106.25 if 'white' in pawn_name else 106.25  # Direction based on pawn color
    promotion_rank = 10.625 if 'white' in pawn_name else 754.375

    # Define board limits
    min_limit = 0
    max_limit = 850  # Assuming board is 850x850 with each cell 106.253
    # Define specific off-limit squares
    off_limit_squares = [(754.376, 116.876), (754.376, 648.12)]

    # Diagonal capturing moves
    for dx in [-106.25, 106.25]:  # Check both diagonals
        new_x = x + dx
        new_y = y + direction

        # Ensure new position is within board bounds and not in off-limit squares
        if min_limit <= new_x <= max_limit and min_limit <= new_y <= max_limit:
            if (new_x, new_y) not in off_limit_squares:
                # Check if there's an opponent's piece at the diagonal position
                target_piece = None
                for piece_type in piece:
                    for piece_name, piece_info in piece[piece_type].items():
                        if piece_info['pos'] == (new_x, new_y) and piece_info['visible']:
                            target_piece = piece_name
                            break
                
                # Capture condition
                if target_piece:
                    if ('white' in pawn_name and 'black' in target_piece) or ('black' in pawn_name and 'white' in target_piece):
                        if new_y == promotion_rank:
                            promotions.append((new_x, new_y))
                        else:
                            moves.append((new_x, new_y))

    # Check moving one square forward
    new_y = y + direction
    if min_limit <= new_y <= max_limit:
        if (x, new_y) not in off_limit_squares:
            forward_move_blocked = False
            for piece_type in piece:
                for piece_name, piece_info in piece[piece_type].items():
                    if piece_info['pos'] == (x, new_y) and piece_info['visible']:
                        forward_move_blocked = True
                        break
            if not forward_move_blocked:
                if new_y == promotion_rank:
                    promotions.append((x, new_y))
                else:
                    moves.append((x, new_y))

    # Check moving two squares forward on first move
    if not pawn_info['has_moved']:
        new_y = y + 2 * direction
        intermediate_y = y + direction
        if min_limit <= new_y <= max_limit:
            if (x, intermediate_y) not in off_limit_squares and (x, new_y) not in off_limit_squares:
                two_step_blocked = False
                for piece_type in piece:
                    for piece_name, piece_info in piece[piece_type].items():
                        if piece_info['pos'] in [(x, intermediate_y), (x, new_y)] and piece_info['visible']:
                            two_step_blocked = True
                            break
                if not two_step_blocked:
                    moves.append((x, new_y))

    # Check for en passant
    if last_move:
        last_piece, last_start, last_end = last_move
        
        # Determine if the piece being checked is an opponent's pawn and if it moved two squares
        if ('white' in pawn_name and 'blackpawn' in last_piece) or ('black' in pawn_name and 'whitepawn' in last_piece):
            if abs(last_start[1] - last_end[1]) == 212.5:  # If last move was a double move
                # Check if the last moved pawn is in an adjacent column and current piece is next to itst
                # print("     ",last_end[0])
                if last_end[0] in [x - 106.25, x + 106.25] and last_end[1] == y:
                    # Calculate the y position for the en passant move
                    en_passant_y = y + direction
                    if min_limit <= en_passant_y <= max_limit:
                        if (last_end[0], en_passant_y) not in off_limit_squares:
                            en_passant_moves.append((last_end[0], en_passant_y))

    # Debug prints
    # print(f"Pawn {pawn_name} at {pawn_info['pos']} moves: {moves}, promotions: {promotions}, en passant: {en_passant_moves}")

    return moves, promotions, en_passant_moves

# Function to get knight moves
def get_knight_moves(knight_name, knight_info):
    """
    Get all possible moves for the knight piece.

    :param knight_name: The name of the knight piece (e.g., 'whiteknight1').
    :param knight_info: Dictionary containing information about the knight piece, including its position.
    :return: List of tuples representing the valid moves for the knight.
    """
    moves = []
    x, y = knight_info['pos']
    knight_moves = [
        (x + 106.25, y + 212.5), (x + 106.25, y - 212.5), (x - 106.25, y + 212.5), (x - 106.25, y - 212.5),
        (x + 212.5, y + 106.25), (x + 212.5, y - 106.25), (x - 212.5, y + 106.25), (x - 212.5, y - 106.25)
    ]

    for move in knight_moves:
        if 0 <= move[0] < 850 and 0 <= move[1] < 850:
            target_square = [(piece_info['pos'], piece_name) for piece_type in piece for piece_name, piece_info in piece[piece_type].items() if piece_info['pos'] == move and piece_info['visible']]
            # print(f"Knight Move: {move}")
            # print(f"Target Square: {target_square}")

            if not target_square:
                moves.append(move)  # Move to an empty square
            elif (target_square and 'white' in knight_name and 'black' in target_square[0][1]) or (target_square and 'black' in knight_name and 'white' in target_square[0][1]):
                moves.append(move)  # Capture opponent's piece
        # else:
            # print(f"Move {move} is out of bounds")

    return moves

# Function to get rook moves
def get_rook_moves(rook_name, rook_info):
    moves = []
    x, y = rook_info['pos']
    directions = [(106.25, 0), (-106.25, 0), (0, 106.25), (0, -106.25)]  # Horizontal and vertical directions

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        while 0 <= nx < 850 and 0 <= ny < 850:
            target_square = [(piece_info['pos'], piece_name) for piece_type in piece for piece_name, piece_info in piece[piece_type].items() if piece_info['pos'] == (nx, ny) and piece_info['visible']]
            if not target_square:
                moves.append((nx, ny))  # Move to an empty square
            else:
                target_piece_name = target_square[0][1]
                if ('white' in rook_name and 'black' in target_piece_name) or ('black' in rook_name and 'white' in target_piece_name):
                    moves.append((nx, ny))  # Capture opponent's piece
                break  # Stop at the first piece (either own or opponent's)
            nx, ny = nx + dx, ny + dy

    return moves

# Function to get queen moves (combining rook and bishop movements)
def get_queen_moves(queen_name, queen_info):
    moves = []
    moves.extend(get_rook_moves(queen_name, queen_info))
    moves.extend(get_bishop_moves(queen_name, queen_info))
    return moves
    
def is_check(all_moves):
    for i in all_moves:
        for item in i:
            if item == piece['king']['whiteking']['pos'] or item == piece['king']['blackking']['pos'] :
                return True
    return False
                      
# Function to get king moves
def get_king_moves(king_name, king_info):
    moves = []
    x, y = king_info['pos']
    king_moves = [
        (x + 106.25, y), (x - 106.25, y), (x, y + 106.25), (x, y - 106.25),
        (x + 106.25, y + 106.25), (x + 106.25, y - 106.25), (x - 106.25, y + 106.25), (x - 106.25, y - 106.25)
    ]

    color = 'white' if 'white' in king_name else 'black'
    
    for move in king_moves:
        if 0 <= move[0] < 850 and 0 <= move[1] < 850:
            # print(move[0],move[1])
            target_square_occupied = False
            target_square_color = None
            
            # Check if the target square is occupied
            for piece_type in piece:
                for piece_name, piece_info in piece[piece_type].items():
                    if piece_info['pos'] == move and piece_info['visible']:
                        target_square_occupied = True
                        target_square_color = 'white' if 'white' in piece_name else 'black'
                        break

            # Ensure the king does not move to a square occupied by its own piece
            if not target_square_occupied or (target_square_occupied and target_square_color != color):
                moves.append(move)  # Add move if the target square is not blocked by its own piece

    # Castling: Check castling rights and add castling moves
    castling_rights_key = f'{color}'
    
    # Helper function to check if the path is clear
    def is_path_clear(start, end, step):
        x_start, y_start = start
        x_end, y_end = end
        x_step, y_step = step
        x, y = x_start + x_step, y_start + y_step
        while (x, y) != (x_end, y_end):
            if any(piece_info['pos'] == (x, y) and piece_info['visible'] for piece_type in piece for piece_info in piece[piece_type].values()):
                return False
            x += x_step
            y += y_step
        return True

    if y == 754.375:  # For white king
        if castling_rights[castling_rights_key]['kingside'] and not has_moved[color]['king'] and not has_moved[color]['kingside_rook']:
            if piece['rook']['whiterook2']['moved'] != True:
                if is_path_clear((x, y), (x + 318.75, y), (106.25, 0)):
                    moves.append((x + 212.5, y))  # White kingside castling
        
        if castling_rights[castling_rights_key]['queenside'] and not has_moved[color]['king'] and not has_moved[color]['queenside_rook'] and piece['rook']['whiterook1']['moved'] != True:
            if is_path_clear((x, y), (x - 425, y), (-106.25, 0)):
                moves.append((x - 212.5, y))  # White queenside castling

    elif y == 10.625:  # For black king
        if castling_rights[castling_rights_key]['kingside'] and not has_moved[color]['king'] and not has_moved[color]['kingside_rook'] and piece['rook']['blackrook2']['moved'] != True:
            if is_path_clear((x, y), (x + 425, y), (106.25, 0)):
                moves.append((x + 212.5, y))  # Black kingside castling
        
        if castling_rights[castling_rights_key]['queenside'] and not has_moved[color]['king'] and not has_moved[color]['queenside_rook'] and piece['rook']['blackrook1']['moved'] != True:
            if is_path_clear((x, y), (x - 318.75, y), (-106.25, 0)):
                moves.append((x - 212.55, y))  # Black queenside castling
    return moves

# Function to get bishop moves
def get_bishop_moves(bishop_name, bishop_info):
    moves = []
    x, y = bishop_info['pos']
    directions = [(106.25, 106.25), (106.25, -106.25), (-106.25, 106.25), (-106.25, -106.25)]  # Diagonal directions
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        # print("while nx: " + str(nx) + " & ny: " +str(ny))
        while 0 <= nx < 850 and 0 <= ny < 850:
            # print("while nx: " + str(nx) + " & ny: " +str(ny))
            target_square = [(piece_info['pos'], piece_name) for piece_type in piece for piece_name, piece_info in piece[piece_type].items() if piece_info['pos'] == (nx, ny) and piece_info['visible']]
            if not target_square:
                # print("not target square")
                moves.append((nx, ny))  # Move to an empty square
            elif (target_square and 'white' in bishop_name and 'black' in target_square[0][1]) or (target_square and 'black' in bishop_name and 'white' in target_square[0][1]):
                # print("Target")
                moves.append((nx, ny))  # Capture opponent's piece
                break
            else:
                # print("bishop_blocked")
                break  # Blocked by another piece
            nx, ny = nx + dx, ny + dy

    return moves  

def move_piece(piece_name, new_position, move, pos):
    global available_moves
    """
    Move the selected piece to a new position and capture any opponent's piece on that position.

    :param piece_name: Name of the piece (e.g., 'whitepawn1').
    :param new_position: Tuple representing the new position (x, y).
    """
    global flag,flag1
    # Remove opponent's piece at the new position, if any
    remove_piece_at_position(new_position)

    # Move the selected piece to the new position
    for piece_type in piece:
        if piece_name in piece[piece_type]:
            start_position = piece[piece_type][piece_name]['pos']
            old_x = piece_info['pos'][0]
            piece[piece_type][piece_name]['pos'] = new_position
            new_x = piece_info['pos'][0]
            # print(f"NEW at {piece_info['pos']} moves: {move}")
            # print(pos)

            # print(piece_type)
            if piece_type == 'pawn':
                piece[piece_type][piece_name]['has_moved'] = True
                if len(move[2]) > 0 and old_x != new_x:
                    remove_piece_at_position(pos)
                if len(move[1]) > 0 and piece_name[0] == 'w':
                    flag = True
                else:
                    flag = False
                if len(move[1]) > 0 and piece_name[0] == 'b':
                    flag1 = True
                else:
                    flag1 = False
            if piece_type == 'king':
                # print(move[0][0])
                for i in move[0]:
                    # print("current index", i)
                    # print(new_position[1])
                    if i == (541.875,754.375) and new_position[1] == 754.375:
                        piece['rook']['whiterook2']['pos'] = (541.875,754.375)
                    if i == (329.375,754.375) and new_position[0] == 754.375:
                        piece['rook']['whiterook1']['pos'] = (329.375,754.375)
                    if i == (541.875, 10.625) and new_position[0] == 10.625:
                        piece['rook']['blackrook2']['pos'] = (541.875, 10.625)
                    if i == (329.375, 10.625) and new_position[0] == 10.625:
                        piece['rook']['blackrook1']['pos'] = (329.375, 10.625)
            
            if piece_type == 'rook':
                piece['rook'][piece_name]['moved'] = True
            
            # Mark king or rook as moved
                
            if piece_name.endswith('king'):
                color = 'white' if piece_name.startswith('white') else 'black'
                has_moved[color]['king'] = True
            elif piece_name.endswith('rook'):
                color = 'white' if piece_name.startswith('white') else 'black'
                if start_position in [(10.625, 754.375), (754.375, 754.375)]:
                    has_moved[color]['kingside_rook'] = True
                elif start_position in [(10.625, 10.625), (754.375, 10.625)]:
                    has_moved[color]['queenside_rook'] = True
            available_moves = ([],[],[])
            break

def promote_into(piece_name,last_move, piece_images):
    global p
    global flag, flag1
    
    """
    Handle pawn promotion process and update piece images.

    Args:
        last_move (tuple): Contains the last move details (piece, old position, new position).
        piece_images (dict): Dictionary of piece images with their positions.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  # Exit the program
        elif event.type == pygame.MOUSEMOTION:
            mouse_xm, mouse_ym = event.pos
            # print(f'{mouse_xm}, {mouse_ym}')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # Define promotion options with their positions
            promotion_options = {
                'queen': (542.125, 435.625),  # Position for queen
                'rook': (435.875, 435.625),   # Position for rook
                'bishop': (329.625, 435.625), # Position for bishop
                'knight': (223.375, 435.625)  # Position for knight
            }
            for piece_type, (pos_x, pos_y) in promotion_options.items():
                # Update the piece type and its image
                if piece_images[0][0] == 'w' and (mouse_x >= 532 and mouse_x <= 636 ) and (mouse_y >= 424 and mouse_y <= 530):
                    # print(piece_type)
                    p = 0
                    a = 'whitequeen' + str(p)
                    # print(mouse_x, mouse_y)
                    PromotionQueenwhite = {a:{'pos': last_move,'moves': [],'visible': True,'image': whitequeen,'color': 0}}
                    piece['queen'].update(PromotionQueenwhite)
                    piece['pawn'][piece_images[0]]['visible'] = False
                    
                    # print(piece['queen'])
                    flag = False
                    flag1 = False
                    p += 1
                    break
                elif piece_images[0][0] == 'b' and (mouse_x >= 532 and mouse_x <= 636 ) and (mouse_y >= 424 and mouse_y <= 530):
                    c = 'blackqueen' + str(p)
                
                    PromotionQueenblack = {c:{'pos': last_move,'moves': [],'visible': True,'image': blackqueen,'color': 1}}
                    piece['queen'].update(PromotionQueenblack)
                    piece['pawn'][piece_images[0]]['visible'] = False
                    # print(piece['queen'])
                    p += 1
                    flag = False
                    flag1 = False
                    break
                elif piece_images[0][0] == 'w' and (mouse_x >= 425 and mouse_x <= 531 ) and (mouse_y >= 426 and mouse_y <= 530):
                    d = 'whiterook' + str(p)
                
                    PromotionRookwhite = {d:{'pos': last_move,'moves': [],'visible': True,'image': whiterook,'moved':True,'color': 0}}
                    piece['rook'].update(PromotionRookwhite)
                    piece['pawn'][piece_images[0]]['visible'] = False
                    # print(piece['rook'])
                    p += 1
                    flag = False
                    flag1 = False
                    break
                elif piece_images[0][0] == 'b' and (mouse_x >= 425 and mouse_x <= 531 ) and (mouse_y >= 426 and mouse_y <= 530):
                    e = 'blackrook' + str(p)
                
                    PromotionRookblack = {e:{'pos': last_move,'moves': [],'visible': True,'image': blackrook,'moved':True,'color': 1}}
                    piece['rook'].update(PromotionRookblack)
                    piece['pawn'][piece_images[0]]['visible'] = False
                    # print(piece['rook'])
                    p += 1
                    flag = False
                    flag1 = False
                    break
                elif piece_images[0][0] == 'w' and (mouse_x >= 319 and mouse_x <= 424 ) and (mouse_y >= 426 and mouse_y <= 530):
                    f = 'whitebishop' + str(p)
                    
                    PromotionBishopwhite = {f:{'pos': last_move,'moves': [],'visible': True,'image': whitebishop,'color': 0}}
                    piece['bishop'].update(PromotionBishopwhite)
                    piece['pawn'][piece_images[0]]['visible'] = False
                    # print(piece['bishop'])
                    flag = False
                    flag1 = False
                    p += 1
                    break
                elif piece_images[0][0] == 'b' and (mouse_x >= 319 and mouse_x <= 424 ) and (mouse_y >= 426 and mouse_y <= 530):
                    g = 'blackbishop' + str(p)
                
                    PromotionBishopblack = {g:{'pos': last_move,'moves': [],'visible': True,'image': blackbishop,'color': 1}}
                    piece['bishop'].update(PromotionBishopblack)
                    piece['pawn'][piece_images[0]]['visible'] = False
                    # print(piece['bishop'])
                    flag = False
                    flag1 = False
                    p += 1
                elif piece_images[0][0] == 'w' and (mouse_x >= 213 and mouse_x <= 318 ) and (mouse_y >= 426 and mouse_y <= 530):
                    h = 'whiteknight' + str(p)
                    
                    PromotionKnightwhite = {h:{'pos': last_move,'moves': [],'visible': True,'image': whiteknight,'color': 0}}
                    piece['knight'].update(PromotionKnightwhite)
                    piece['pawn'][piece_images[0]]['visible'] = False
                    # print(piece['knight'])
                    flag = False
                    flag1 = False
                    p += 1
                    break
                elif piece_images[0][0] == 'b' and (mouse_x >= 213 and mouse_x <= 318 ) and (mouse_y >= 426 and mouse_y <= 530):
                    i = 'blackknight' + str(p)
                
                    PromotionKnightblack = {i:{'pos': last_move,'moves': [],'visible': True,'image': blackknight,'color': 1}}
                    piece['knight'].update(PromotionKnightblack)
                    piece['pawn'][piece_images[0]]['visible'] = False
                    # print(piece['knight'])
                    p += 1
                    flag = False
                    flag1 = False
                    break

def is_under_threat(pos, color):
    opponent_color = (color + 1) % 2
    for piece_type in piece:
        for piece_name, piece_info in piece[piece_type].items():
            if piece_info['color'] == opponent_color and piece_info['visible']:
                if pos in piece_info['moves']:
                    return True
    return False

def is_king_in_check(color):
    for piece_name, piece_info in piece['king'].items():
        if piece_info['color'] == color and piece_info['visible']:
            return is_under_threat(piece_info['pos'], color)
    return False

def filter_legal_moves(moves, piece_name, piece_type):
    legal_moves = []
    original_pos = piece[piece_type][piece_name]['pos']
    for move in moves:
        piece[piece_type][piece_name]['pos'] = move
        if not is_king_in_check(piece[piece_type][piece_name]['color']):
            legal_moves.append(move)
        piece[piece_type][piece_name]['pos'] = original_pos
    return legal_moves

def check_all(check):
    all_moves = []
    for i in piece:
        for item in piece[i]:
            if turn == 0: 
                if piece[i][item]['color'] == 1:
                    if i == 'pawn':
                        a,b,c = get_pawn_moves(item, piece[i][item], last_move)
                        all_moves.append(a)
                        all_moves.append(b)
                        all_moves.append(c)
                    if i == 'knight':
                        all_moves.append(get_knight_moves(item, piece[i][item]))
                    if i == 'rook':
                        all_moves.append(get_rook_moves(item, piece[i][item]))
                    if i == 'bishop':
                        all_moves.append(get_bishop_moves(item, piece[i][item]))
                    if i == 'queen':
                        all_moves.append(get_queen_moves(item, piece[i][item]))
                check = is_check(all_moves)
                # print(check)
            if turn == 1: 
                if piece[i][item]['color'] == 0:
                    if i == 'pawn':
                        a,b,c = get_pawn_moves(item, piece[i][item], last_move)
                        all_moves.append(a)
                        all_moves.append(b)
                        all_moves.append(c)
                    if i == 'knight':
                        all_moves.append(get_knight_moves(item, piece[i][item]))
                    if i == 'rook':
                        all_moves.append(get_rook_moves(item, piece[i][item]))
                    if i == 'bishop':
                        all_moves.append(get_bishop_moves(item, piece[i][item]))
                    if i == 'queen':
                        all_moves.append(get_queen_moves(item, piece[i][item]))                                        
                check = is_check(all_moves)
    return all_moves, check

def is_checkmate(color):
    pass
    # for piece_type in piece:
    #     for piece_name, piece_info in piece[piece_type].items():
    #         if piece_info['color'] == color and piece_info['visible']:
    #             legal_moves = filter_legal_moves(piece_info['moves'], piece_name, piece_type)
    #             if legal_moves:
    #                 return False
    # return True
    # for i in piece:
    #         for item in piece[i]:
    #             if i == 'king' and check:
    #                 if len(get_king_moves(item, piece[i][item])) == 0:
    #                     print('Checkmate')
    #                     running = False
    #                     checkmate = True

def find_piece(move):
    for piece_type in piece:
        for piece_name, piece_info in piece[piece_type].items():
            if piece_info['pos'] == move and piece_type != 'king':
                return piece_type, piece_name
    return '', ''

def pre_king_moves(selected_piece, selected_piece_type, king_move):
    moves = []
    ch = False
    temp_pos = piece[selected_piece_type][selected_piece]['pos']
    piece[selected_piece_type][selected_piece]['pos'] = king_move
    
    piece_type, piece_name = find_piece(king_move)
    captured_piece_info = None
    
    if piece_type != '' and piece_name != '' and piece_type != selected_piece:
        captured_piece_info = piece[piece_type][piece_name]
        captured_piece_info['visible'] = False

    all_moves, ch = check_all(ch)
    
    for piece_moves in all_moves:
        for move in piece_moves:
            if move == king_move:
                moves.append(move)

    # Restore the original position and visibility
    piece[selected_piece_type][selected_piece]['pos'] = temp_pos
    if captured_piece_info is not None:
        captured_piece_info['visible'] = True
    
    return moves

# Main game loop
running = True
selected_piece = None
available_moves = ([], [], [])  # Moves, promotions, en passant moves
last_move = None
flag = False
flag1 = False
choose = False
p = 3
flag2 = False
turn = 0
checkmate = False
check = False
will_check = False
all_moves = []

while running:
    if choose:
        # available_moves = ([],[],[])
        promote_into(piece_name,move,last_move)
        choose = False
        flag2 = True
    else:
        for event in pygame.event.get():
            if checkmate:
                break
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                global mouse_x,mouse_y
                mouse_x, mouse_y = event.pos
                # Check if the click is on an available move position
                move_selected = False
                for move in available_moves[0] + available_moves[1] + available_moves[2]:
                    move_x, move_y = move
                    if move_x <= mouse_x < move_x + 106.25 and move_y <= mouse_y < move_y + 106.25:
                        if selected_piece:
                            # Check if `last_move` is not None before assigning to `temp`
                            temp = last_move if last_move else (None, None, None)
                            last_move = (selected_piece, piece[selected_piece_type][selected_piece]['pos'], (move_x, move_y))
                            pos = temp[2] if temp else None
                            move_piece(selected_piece, (move_x, move_y), available_moves, pos)

                            # Update castling rights if a king or rook moves
                            update_castling_rights(last_move, castling_rights)
                            
                            # Deselect piece and reset available moves
                            selected_piece = None
                            available_moves = ([], [], [])
                            move_selected = True
                            turn += 1
                            turn  %= 2
                            break

                if not move_selected:
                    # Check if a piece was clicked and select it
                    selected_piece = None
                    for piece_type in piece:
                        for piece_name, piece_info in piece[piece_type].items():
                            piece_x, piece_y = piece_info['pos']
                            if piece_x <= mouse_x < piece_x + 106.25 and piece_y <= mouse_y < piece_y + 106.25 and piece_info['visible'] and piece[piece_type][piece_name]['color'] == turn:
                                selected_piece = piece_name
                                selected_piece_type = piece_type
                                break
                        if selected_piece:
                            break
                    
                    # Get available moves for the selected piece
                    if selected_piece and piece[piece_type][piece_name]['color'] == turn:
                        if selected_piece_type == 'pawn' :
                            available_moves = get_pawn_moves(selected_piece, piece[selected_piece_type][selected_piece], last_move)
                        elif selected_piece_type == 'knight':
                            available_moves = (get_knight_moves(selected_piece, piece[selected_piece_type][selected_piece]), [], [])
                        elif selected_piece_type == 'rook':
                            available_moves = (get_rook_moves(selected_piece, piece[selected_piece_type][selected_piece]), [], [])
                        elif selected_piece_type == 'bishop':
                            available_moves = (get_bishop_moves(selected_piece, piece[selected_piece_type][selected_piece]), [], [])
                        elif selected_piece_type == 'queen':
                            available_moves = (get_queen_moves(selected_piece, piece[selected_piece_type][selected_piece]), [], [])
                        elif selected_piece_type == 'king':
                            available_moves = (get_king_moves(selected_piece, piece[selected_piece_type][selected_piece]), [], [])

                            for item in all_moves:
                                for move in item:
                                    for replace in available_moves[0]:
                                        if replace == move:
                                            available_moves[0].remove(replace)
                                            if len(available_moves[0]) == 0:
                                                running = False
                                                break
                            print(available_moves[0])
                            if len(available_moves[0]) == 0:
                                pass           
                            elif len(available_moves[0]) > 1:
                                for i in range (len(available_moves[0])-1):
                                    king_moves = pre_king_moves(selected_piece,selected_piece_type,available_moves[0][i])
                                    for move in king_moves:
                                        for replace in available_moves[0]:
                                            if replace == move:
                                                available_moves[0].remove(replace)
                                                if len(available_moves[0]) == 0:
                                                    running = False
                                                    break
                            else:
                                king_moves = pre_king_moves(selected_piece,selected_piece_type,available_moves[0][0])
                                for move in king_moves:
                                    for replace in available_moves[0]:
                                        if replace == move:
                                            available_moves[0].remove(replace)
                                            if len(available_moves[0]) == 0:
                                                running = False
                                                break
                            available_moves[0]          
                all_moves, check = check_all(check)
                        
        # Redraw the board and pieces
        blit_pieces(available_moves)
        
# Quit Pygame
pygame.quit()