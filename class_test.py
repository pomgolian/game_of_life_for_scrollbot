import random
import time


class Life:
    def __init__(self, h_boxes=17, v_boxes=7):
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

    def __repr__(self):
        return 'creates dictionary called life containing\n1s and 0s representing live and dead cells'

    def check_repeating_iteration(self, life):
        self.life = life
        if self.life in self.life_list:
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
            fw, bw, up, dn = 1, -1, self.vertical_boxes, -self.vertical_boxes
            # set up our edge cases for cell neighbors
            if cell % self.horizontal_boxes == 0:
                bw = self.horizontal_boxes - 1
            if (cell + 1) % self.horizontal_boxes == 0:
                fw = -self.horizontal_boxes + 1
            if (cell - self.vertical_boxes) < 0:
                dn = (self.vertical_boxes * self.horizontal_boxes) - self.horizontal_boxes
            if (cell + self.vertical_boxes) > (self.vertical_boxes * self.horizontal_boxes) - 1:
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
        if self.check_repeating_iteration(self.life):
            return True


game_on = True


def run_game():
    global game_on
    iterations = 0
    while game_on:
        life = 'unique'
        game = Life(2, 1)
        while life == 'unique':
            if game.update_life():
                print('Current game iteration was {}'.format(game.iteration))
                if game.iteration > iterations:
                    iterations = game.iteration
                for key in game.life:
                    print(game.life[key], end='')
                    if (key + 1) % 17 == 0:
                        print('')
                print('------')
                life = 'repeating'
                print('Highest game iterations were {}'.format(iterations))
                print('------')
            #time.sleep(0.2)


if __name__ == '__main__':
    run_game()