import pygame
import random
import time

ORANGE = {'light': (255, 165, 0), 'dark': (255, 140, 0)}
WHITE = {'light': (255, 255, 255), 'dark': (245, 245, 245)}
GREEN = {'light': (0, 255, 0), 'dark': (0, 100, 0)}
RED = {'light': (255, 0, 0), 'dark': (139, 0, 0)}
PINK = {'light': (255, 192, 203), 'dark': (255, 20, 147)}

list_of_colors = [ORANGE, WHITE, GREEN, RED, PINK]

surface_width = 600
surface_height = 650
square_sz = int(500 / 25)

pygame.init()
clock = pygame.time.Clock()
main_surface = pygame.display.set_mode((surface_width, surface_height))
TURNS = 50

class Game:
    def __init__(self):

        self.background_color = (0, 200, 255)
        self.board_size = (500, 500)
        self.buttons = list()
        self.board = list()
        self.create_board()
        self.current_color = self.board[0][0].color
        self.matched_squares = [[None] * 25 for _ in range(25)]
        self.number_of_tries_total = TURNS
        self.attempts_made = 0

        self.tries = list()
        self.matched_squares[0][0] = self.board[0][0]
        self.check_matches(self.current_color)

    def create_board(self):
        for row_i in range(int(500 / square_sz)):
            self.board.append(
                [Square(random.choice(list_of_colors)['light'], row_i, col_i) for col_i in range(int(self.board_size[0] / 20))])

    def reset_game(self, color=None):
        self.matched_squares = list()
        self.board = list()
        self.create_board()
        self.current_color = self.board[0][0].color
        self.matched_squares = [[None] * 25 for _ in range(25)]
        self.number_of_tries_total = TURNS
        self.attempts_made = 0

        self.tries = list()
        self.matched_squares[0][0] = self.board[0][0]
        self.check_matches(self.current_color)

    def add_squares_to_screen(self, screen):
        for row in self.board:
            for item in row:
                screen.fill(item.color, item.rect)

    def add_buttons_to_screen(self, screen, events):
        for ind, color in enumerate(list_of_colors):
            self.buttons.append(button(ind * 75 + 30, 550, 50, 50,
                                       color['light'], color['dark'], events, action=self.take_turn))

    def add_turns_to_screen(self, screen):
        self.tries = [Square((128, 0, 128), 27, 1.08 * num)
                      for num in range(self.number_of_tries_total - self.attempts_made)]
        for square in self.tries:
            screen.fill(square.color, square.rect)

    def take_turn(self, color):
        try:
            self.check_matches(color)
            self.attempts_made += 1
            self.add_turns_to_screen(main_surface)
        except IndexError:
            pass

    def check_matches(self, color):
        if not color:
            color = self.current_color

        for ind_i, row in enumerate(self.matched_squares):
            for col_i, square in enumerate(row):
                if square:
                    square.color = color
                    if col_i >= 0 and col_i < 24:   # check if square matches the next one in the column
                        if square.check_for_match(self.board[ind_i][col_i + 1]):
                            self.board[ind_i][col_i + 1].color = color
                            self.matched_squares[ind_i][col_i +
                                                        1] = self.board[ind_i][col_i + 1]
                    if col_i >= 1 and col_i < 24:   # check if square matches the one behind it in the column
                        if square.check_for_match(self.board[ind_i][col_i - 1]):
                            self.board[ind_i][col_i - 1].color = color
                            self.matched_squares[ind_i][col_i -
                                                        1] = self.board[ind_i][col_i - 1]
                    if ind_i >= 0 and ind_i < 24:   # check if square matches the one below it.
                        if square.check_for_match(self.board[ind_i + 1][col_i]):
                            self.board[ind_i + 1][col_i].color = color
                            self.matched_squares[ind_i +
                                                 1][col_i] = self.board[ind_i + 1][col_i]
                    if ind_i >= 1 and ind_i < 25:    # check if square matches the one above it.
                        if square.check_for_match(self.board[ind_i - 1][col_i]):
                            self.board[ind_i - 1][col_i].color = color
                            self.matched_squares[ind_i -
                                                 1][col_i] = self.board[ind_i - 1][col_i]

    def check_winner(self, events):
        for row in self.matched_squares:
            if None in row:
                return False
        return self.winner(events)

    def winner(self, events):
        button(500 // 2, 500 // 2, 150, 150, (0, 0, 0),
               (0, 0, 0), events, action=None, msg="You Win!")
        button(500 // 2, 280, 100, 100, (0, 0, 0), (0, 0, 0),
               events, self.reset_game, msg="Play Again")

    def check_loser(self, events):
        if self.attempts_made > self.number_of_tries_total:
            return self.loser(events)

    def loser(self, events):
        button(500 // 2, 500 // 2, 150, 150, (0, 0, 0),
               (0, 0, 0), events, None, "You Lose!")
        time.sleep(3)
        self.reset_game()


class Square:
    def __init__(self, color, row_i, col_i):
        self.color = color
        self.rect = (int(row_i * square_sz),
                     int(col_i * square_sz), square_sz, square_sz)
        self.matched = False

    def change_color(self, new_color):
        self.color = new_color

    def check_for_match(self, other):
        if self.color == other.color:
            return True
        return False


def button(x, y, w, h, inactive, active, events, action=None, msg=None):
    button_rect = pygame.Rect(x, y, w, h)
    pos = pygame.mouse.get_pos()

    if msg:
        largeText = pygame.font.Font('freesansbold.ttf', 40)
        TextSurf, _ = text_objects(msg, largeText)
        main_surface.blit(TextSurf, button_rect)

    if button_rect.collidepoint(pos):
        if not msg:
            main_surface.fill(active, button_rect)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and action:
                action(inactive)
                clock.tick(60)
    if not msg:
        main_surface.fill(inactive, button_rect)


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def main():
    game = Game()
    while True:
        main_surface.fill((0, 200, 255))
        game.add_squares_to_screen(main_surface)
        game.add_turns_to_screen(main_surface)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        game.add_buttons_to_screen(main_surface, events)

        button(50, 600, 200, 200, (0, 0, 0), (0, 0, 0),
               events, game.reset_game, 'Reset Game')
        game.check_winner(events)
        game.check_loser(events)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
