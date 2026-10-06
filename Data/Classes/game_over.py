from pathlib import Path

import pygame


def show_game_over(display, winner, duration_ms=5000):
    #Show a winner-coloured screen for the requested number of milliseconds.
    winner = winner.strip().lower()
    if winner not in {"white", "black"}:
        raise ValueError("winner must be 'White' or 'Black'")

    piece_prefix = "w" if winner == "white" else "b"
    background = (255, 255, 255) if winner == "white" else (0, 0, 0)
    text_colour = (0, 0, 0) if winner == "white" else (255, 255, 255)
    width, height = display.get_size()

    image_dir = Path(__file__).resolve().parents[1] / "imgs"

    def load_piece(notation, size):
        image = pygame.image.load(str(image_dir / f"{piece_prefix}{notation}.png"))
        return pygame.transform.smoothscale(image, (size, size))

    corner_size = min(110, width // 7, height // 6)
    center_size = min(94, width // 8, height // 7)
    pieces = {
        "bishop": load_piece("B", corner_size),
        "knight": load_piece("N", corner_size),
        "rook": load_piece("R", corner_size),
        "pawn": load_piece("P", corner_size),
        "queen": load_piece("Q", center_size),
        "king": load_piece("K", center_size),
    }

    margin = max(18, corner_size // 5)
    placements = {
        "bishop": (margin, margin),
        "knight": (width - margin - corner_size, margin),
        "rook": (margin, height - margin - corner_size),
        "pawn": (width - margin - corner_size, height - margin - corner_size),
    }

    message = f"{winner.title()} has won!!!"
    font_size = 64
    font = pygame.font.Font(None, font_size)
    while font.size(message)[0] + center_size * 2 + 64 > width - margin * 2 and font_size > 28:
        font_size -= 2
        font = pygame.font.Font(None, font_size)

    message_image = font.render(message, True, text_colour)
    message_rect = message_image.get_rect(center=(width // 2, height // 2))
    queen_rect = pieces["queen"].get_rect(
        midright=(message_rect.left - 24, height // 2)
    )
    king_rect = pieces["king"].get_rect(
        midleft=(message_rect.right + 24, height // 2)
    )

    clock = pygame.time.Clock()
    end_time = pygame.time.get_ticks() + duration_ms
    while pygame.time.get_ticks() < end_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Let the menu receive the close event after this screen returns.
                pygame.event.post(event)
                return

        display.fill(background)
        for name, position in placements.items():
            display.blit(pieces[name], position)
        display.blit(pieces["queen"], queen_rect)
        display.blit(message_image, message_rect)
        display.blit(pieces["king"], king_rect)
        pygame.display.flip()
        clock.tick(60)
