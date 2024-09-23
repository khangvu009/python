import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
CARD_WIDTH = 57
CARD_HEIGHT = 82
PADDING = 10
ROTATED_CARD_WIDTH = CARD_HEIGHT  # Width after 90-degree rotation
ROTATED_CARD_HEIGHT = CARD_WIDTH  # Height after 90-degree rotation
BOT_CARD_PADDING = 5  # Padding for bot cards to make them closer

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mậu Binh")

# Define suits and ranks
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
RANK_VALUES = {rank: i for i, rank in enumerate(RANKS)}

# Load card images
def load_card_images():
    card_images = {}
    for suit in SUITS:
        for rank in RANKS:
            image_path = f'{rank}_of_{suit}.png'
            card_image = pygame.image.load(image_path)
            card_image = pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))
            card_images[(rank, suit)] = card_image
    card_back_image = pygame.image.load('card_back.png')
    card_back_image = pygame.transform.scale(card_back_image, (CARD_WIDTH, CARD_HEIGHT))
    card_images["back"] = card_back_image
    
    # Load the rotated back card image
    card_back_rotate_image = pygame.image.load('card_back_rotate.png')
    card_back_rotate_image = pygame.transform.scale(card_back_rotate_image, (ROTATED_CARD_WIDTH, ROTATED_CARD_HEIGHT))
    card_images["back_rotate"] = card_back_rotate_image
    
    return card_images

card_images = load_card_images()

# Rotate card images
def rotate_card_images(card_images):
    rotated_images = {}
    for key, image in card_images.items():
        if key != "back" and key != "back_rotate":
            rotated_images[key] = pygame.transform.rotate(image, 90)
        else:
            rotated_images[key] = image
    return rotated_images

rotated_card_images = rotate_card_images(card_images)

# Card class
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.image = card_images[(rank, suit)]
        self.rotated_image = rotated_card_images[(rank, suit)]
        self.rect = self.image.get_rect()

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

# Deck class
class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

# Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.arranged_hands = {"front": [], "middle": [], "back": []}

    def receive_card(self, card):
        self.hand.append(card)

    def arrange_cards(self):
        self.arranged_hands["front"] = self.hand[:3]
        self.arranged_hands["middle"] = self.hand[3:8]
        self.arranged_hands["back"] = self.hand[8:]

    def swap_cards(self, card1, card2):
        idx1 = self.hand.index(card1)
        idx2 = self.hand.index(card2)
        self.hand[idx1], self.hand[idx2] = self.hand[idx2], self.hand[idx1]

    def is_valid_arrangement(self):
        return (
            self.evaluate_hand(self.arranged_hands["front"]) <=
            self.evaluate_hand(self.arranged_hands["middle"]) <=
            self.evaluate_hand(self.arranged_hands["back"])
        )

    def evaluate_hand(self, hand):
        return sum(RANK_VALUES[card.rank] for card in hand)

# Game setup
deck = Deck()
players = [Player("Human Player"), Player("Bot 1"), Player("Bot 2"), Player("Bot 3")]

# Deal cards to players
for _ in range(13):
    for player in players:
        player.receive_card(deck.deal())

# Automatically arrange cards for bots
for player in players[1:]:
    player.arrange_cards()

# Function to handle card arrangement for human player
def arrange_human_cards(human_player):
    human_player.arrange_cards()

arrange_human_cards(players[0])

# Define card positions for player and bots
def calculate_positions(start_x, start_y, num_cards, padding, rotate=False):
    positions = []
    for j in range(num_cards):
        if rotate:
            x = start_x
            y = start_y - j * (ROTATED_CARD_HEIGHT + padding)
        else:
            x = start_x + j * (CARD_WIDTH + padding)
            y = start_y
        positions.append((x, y))
    return positions

# Player card positions
player_card_positions = calculate_positions(50, SCREEN_HEIGHT // 2 - CARD_HEIGHT // 2, 13, PADDING)

# Left and right opponent deck positions with rotated back cards
left_opponent_deck_positions = calculate_positions(
    50,
    SCREEN_HEIGHT // 2 - ROTATED_CARD_HEIGHT // 2,
    3,
    BOT_CARD_PADDING,
    rotate=True
)

right_opponent_deck_positions = calculate_positions(
    SCREEN_WIDTH - 50 - ROTATED_CARD_WIDTH,
    SCREEN_HEIGHT // 2 - ROTATED_CARD_HEIGHT // 2,
    3,
    BOT_CARD_PADDING,
    rotate=True
)

# Define bot card positions
bot_hand_positions = {
    "front": {
        "Bot 1": calculate_positions(SCREEN_WIDTH - 100 - (ROTATED_CARD_WIDTH + BOT_CARD_PADDING), SCREEN_HEIGHT // 2 - 3 * ROTATED_CARD_HEIGHT - 2 * BOT_CARD_PADDING, 3, BOT_CARD_PADDING, rotate=True),
        "Bot 2": calculate_positions(100, SCREEN_HEIGHT // 2 - 3 * ROTATED_CARD_HEIGHT - 2 * BOT_CARD_PADDING, 3, BOT_CARD_PADDING, rotate=True),
        "Bot 3": calculate_positions(SCREEN_WIDTH // 2 - 3 * (CARD_WIDTH + BOT_CARD_PADDING) // 2, 50, 3, BOT_CARD_PADDING)
    },
    "middle": {
        "Bot 1": calculate_positions(SCREEN_WIDTH - 100 - (ROTATED_CARD_WIDTH + BOT_CARD_PADDING), SCREEN_HEIGHT // 2 - ROTATED_CARD_HEIGHT - BOT_CARD_PADDING, 5, BOT_CARD_PADDING, rotate=True),
        "Bot 2": calculate_positions(100, SCREEN_HEIGHT // 2 - ROTATED_CARD_HEIGHT - BOT_CARD_PADDING, 5, BOT_CARD_PADDING, rotate=True),
        "Bot 3": calculate_positions(SCREEN_WIDTH // 2 - 5 * (CARD_WIDTH + BOT_CARD_PADDING) // 2, 50 + CARD_HEIGHT + BOT_CARD_PADDING, 5, BOT_CARD_PADDING)
    },
    "back": {
        "Bot 1": calculate_positions(SCREEN_WIDTH - 100 - (ROTATED_CARD_WIDTH + BOT_CARD_PADDING), SCREEN_HEIGHT // 2 + ROTATED_CARD_HEIGHT + BOT_CARD_PADDING, 5, BOT_CARD_PADDING, rotate=True),
        "Bot 2": calculate_positions(100, SCREEN_HEIGHT // 2 + ROTATED_CARD_HEIGHT + BOT_CARD_PADDING, 5, BOT_CARD_PADDING, rotate=True),
        "Bot 3": calculate_positions(SCREEN_WIDTH // 2 - 5 * (CARD_WIDTH + BOT_CARD_PADDING) // 2, 50 + 2 * (CARD_HEIGHT + BOT_CARD_PADDING), 5, BOT_CARD_PADDING)
    }
}

# Define areas for arranging hands
hand_areas = {
    "front": pygame.Rect(SCREEN_WIDTH // 2 - (CARD_WIDTH + PADDING) * 1.5, SCREEN_HEIGHT - 3 * CARD_HEIGHT - 30, (CARD_WIDTH + PADDING) * 3, CARD_HEIGHT + 20),
    "middle": pygame.Rect(SCREEN_WIDTH // 2 - (CARD_WIDTH + PADDING) * 2.5, SCREEN_HEIGHT - 2 * CARD_HEIGHT - 20, (CARD_WIDTH + PADDING) * 5, CARD_HEIGHT + 20),
    "back": pygame.Rect(SCREEN_WIDTH // 2 - (CARD_WIDTH + PADDING) * 2.5, SCREEN_HEIGHT - CARD_HEIGHT - 10, (CARD_WIDTH + PADDING) * 5, CARD_HEIGHT + 20)
}

# Main game loop
running = True
show_bot_cards = False
error_message = ""
selected_for_swap = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:  # Left click
                clicked_card = None
                for card in players[0].hand:
                    if card.rect.collidepoint(pos):
                        clicked_card = card
                        break
                if clicked_card:
                    if len(selected_for_swap) == 1:
                        card1 = selected_for_swap[0]
                        card2 = clicked_card
                        players[0].swap_cards(card1, card2)
                        selected_for_swap = []
                    else:
                        selected_for_swap.append(clicked_card)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Press Enter to finalize arrangement and reveal bot cards
                if players[0].is_valid_arrangement():
                    show_bot_cards = True
                else:
                    error_message = "Invalid arrangement! Ensure back > middle > front."

    # Clear screen
    screen.fill((0, 128, 0))  # Green background

    # Draw deck for the human player at the left side of the screen
    for j, card in enumerate(players[0].hand):
        card.rect.topleft = player_card_positions[j]
        if card in selected_for_swap:
            pygame.draw.rect(screen, (255, 0, 0), card.rect.inflate(4, 4), 2)
        screen.blit(card.image, card.rect)

    # Draw arranged cards for the human player
    for area, rect in hand_areas.items():
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)  # Draw area rectangle
        for card in players[0].arranged_hands[area]:
            card.rect.topleft = rect.topleft
            card.rect.x += players[0].arranged_hands[area].index(card) * (CARD_WIDTH + PADDING)
            screen.blit(card.image, card.rect)

    # Draw left opponent's deck with rotated back cards
    for idx, pos in enumerate(left_opponent_deck_positions):
        screen.blit(card_images["back_rotate"], pos)

    # Draw right opponent's deck with rotated back cards
    for idx, pos in enumerate(right_opponent_deck_positions):
        screen.blit(card_images["back_rotate"], pos)

    # Draw bot players' arranged cards
    for bot_name in ["Bot 1", "Bot 2", "Bot 3"]:
        bot = players[int(bot_name[-1])]
        for area in ["front", "middle", "back"]:
            positions = bot_hand_positions[area][bot_name]
            for pos in positions:
                if area == "front" or area == "middle":
                    screen.blit(card_images["back_rotate"], pos)
                else:
                    screen.blit(card_images["back"], pos)

    # Draw error message if any
    if error_message:
        font = pygame.font.Font(None, 36)
        text = font.render(error_message, True, (255, 0, 0))
        screen.blit(text, (50, SCREEN_HEIGHT - 50))

    pygame.display.flip()

pygame.quit()
