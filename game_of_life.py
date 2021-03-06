import random
import scrollphathd as sphd
import time
import shelve # for saving our winning game


class Life:
    def __init__(self, h_boxes=17, v_boxes=7): # use a grid of 17 x 7 for scrollbot
        self.life_list = []
        self.iteration = 0
        self.life = {}
        self.horizontal_boxes = h_boxes
        self.vertical_boxes = v_boxes
        self.life_key = 0
        for y in range(0, self.horizontal_boxes):
            for x in range(0, self.vertical_boxes):
                self.life[self.life_key] = random.randint(0, 1)
                self.life_key += 1
        self.initial_sequence = self.life  # keep the initial sequence so can be shelved if it is a winning starter

    def __repr__(self):
        return 'creates dictionary called life containing\n1s and 0s representing live and dead cells'

    def check_repeating_iteration(self, life):
        self.life = life
        if self.life in self.life_list:  # if our life dict has appeared before, we are in a repeating sequence
            return True
        self.life_list.append(self.life)

    def update_life(self):
        # actual logic of the game
        # Dead from starvation if < 2 neighbors
        # Continue living if 2 or 3 neighbors
        # Dead from overcrowding if > 3 neighbors
        # Become alive from reproduction if 3 neighbors
        new_life = {}
        for cell in self.life:
            # set our defaults for cell neighbors
            fw, bw, up, dn = 1, -1, self.horizontal_boxes, -self.horizontal_boxes
            # set up our edge cases for cell neighbors
            if cell % self.horizontal_boxes == 0:  # means we are on left edge of grid
                bw = self.horizontal_boxes - 1

            if (cell + 1) % self.horizontal_boxes == 0:  # means we are on right edge of grid
                fw = -self.horizontal_boxes + 1

            if (cell - self.horizontal_boxes) < 0:  # means we are on bottom edge
                dn = (self.vertical_boxes * self.horizontal_boxes) - self.horizontal_boxes

            if (cell + self.horizontal_boxes) > (self.vertical_boxes * self.horizontal_boxes) - 1:  # means we are on the top edge
                up = self.horizontal_boxes - ((self.vertical_boxes * self.horizontal_boxes) - cell) - cell

            # now we can count the neighbor score
            score = self.life[cell + fw] + self.life[cell + bw] + self.life[cell + up] + self.life[cell + dn] + \
                    self.life[cell + up + fw] + self.life[cell + up + bw] + self.life[cell + dn + fw] + \
                    self.life[cell + dn + bw]
            if score < 2:
                new_life[cell] = 0
            if score == 2:
                new_life[cell] = self.life[cell]
            if score == 3:
                new_life[cell] = 1
            if score > 3:
                new_life[cell] = 0
        self.life = new_life
        self.iteration += 1
        if self.check_repeating_iteration(self.life):  # return status of the new life
            return 'repeating'
        else:
            return 'unique'


def display_life(current_game):
    sphd.clear() # blank the screen
    for key in current_game: # set our new pixels
        if current_game[key] == 1: # if 1, then light up the LED
            # find Y axis value
            y = key//17
            # find X axis
            x = key - (y * 17)
            sphd.set_pixel(x, y, 1)  # set a brightness of 1 seeing as our default is already .25 and it is cumulative
    sphd.show()  # show the new screen


def display_scroll_text(text, display_time=5):
    update_time = 0.05  # scroll speed in seconds per pixel
    sphd.clear()  # blank the screen ready to write some text
    sphd.write_string(text)
    for t in range(int(display_time / update_time)):
        sphd.show()
        sphd.scroll(1)
        time.sleep(update_time)


def save_game(high_score, initial_grid):
    with shelve.open('best_game', 'c') as shelf:
        shelf['high_score'] = high_score
        shelf['initial_grid'] = initial_grid


def get_highest_score_game():
    with shelve.open('best_game', 'r') as shelf:
        high_score = shelf['high_score']
        initial_grid = shelf['initial_grid']
    return high_score, initial_grid
