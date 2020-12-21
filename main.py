import random
import PySimpleGUI as sg
import time


def main(horizontal_boxes=3, vertical_boxes=3, box_size=10):
    grid_x = horizontal_boxes * box_size
    grid_y = vertical_boxes * box_size
    layout = [[sg.Graph(canvas_size=(400, 400), graph_bottom_left=(0, 0), graph_top_right=(grid_x, grid_y),
                        background_color='white', key='graph', enable_events=True)],
              [sg.Button('Go!', key='-GO-'), sg.Button('Stop', key='-STOP-'), sg.Button('Clear Cells', key='-CLEAR-'),
               sg.Button('Exit', key='-EXIT-')]]
    window = sg.Window('Game of life', layout, grab_anywhere=False).Finalize()
    graph = window['graph']

    # create initial life dict
    life = create_life_dict(grid_x, grid_y, box_size)
    # create grid ready to populate, initial will be all white as life is all 0
    create_grid(graph, grid_x, grid_y, box_size, life)

    while True:
        event, values = window.read()
        if event == '-GO-':
            iterations = 0
            loop = True
            while loop:
                event, values = window.read(timeout=0)
                if event == '-EXIT-':
                    exit()
                if event == '-STOP-':
                    loop = False
                    print(iterations)
                life = kill_or_create_life(life)
                life_key = 0
                graph.erase()
                for y in range(0, grid_y, box_size):
                    for x in range(0, grid_x, box_size):
                        if life[life_key]:
                            cell_colour = 'yellow'
                        else:
                            cell_colour = 'white'
                        graph.DrawRectangle((x, y), (x + box_size, y + box_size), line_color='black',
                                            fill_color=cell_colour)
                        life_key += 1
                window.refresh()
                time.sleep(.3)
                iterations += 1
        if event == '-EXIT-':
            exit()
        if event == '-CLEAR-':
            graph.Erase()
            life = create_life_dict(grid_x, grid_y, box_size)
            create_grid(graph, grid_x, grid_y, box_size, life)
        if event is None:
            exit()
        mouse = values['graph']
        if event == 'graph':
            lower_left_x = mouse[0] - mouse[0]%box_size
            lower_left_y = mouse[1] - mouse[1]%box_size
            select_key = int((lower_left_x/box_size) + (lower_left_y/box_size)*(grid_x/box_size))
            if life[select_key] == 0:
                life[select_key] = 1
                graph.DrawRectangle((lower_left_x, lower_left_y), (lower_left_x + box_size, lower_left_y + box_size),
                                    line_color='black', fill_color='yellow')
            else:
                life[select_key] = 0
                graph.DrawRectangle((lower_left_x, lower_left_y), (lower_left_x + box_size, lower_left_y + box_size),
                                    line_color='black', fill_color='white')


# initial life dictionary that matches grid size
def create_life_dict(grid_x, grid_y, box_size):
    life = {}
    life_key = 0
    for y in range(0, grid_y, box_size):
        for x in range(0, grid_x, box_size):
            life[life_key] = 0 #random.randint(0, 1)
            life_key += 1
    return life


def create_grid(graph, grid_x, grid_y, box_size, life):
    life_key = 0
    graph.Erase()
    for y in range(0, grid_y, box_size):
        for x in range(0, grid_x, box_size):
            if life[life_key]:
                cell_colour = 'yellow'
            else:
                cell_colour = 'white'
            graph.DrawRectangle((x, y), (x + box_size, y + box_size), line_color='black', fill_color=cell_colour)
            life_key += 1


# pass a dictionary to this function to return a new dict
def kill_or_create_life(life):
    # actual logic of the game
    # Dead from starvation if < 2 neighbors
    # Continue living if 2 or 3 neighbors
    # Dead from overcrowding if > 3 neighbors
    # Become alive from reproduction if 3 neighbors
    new_life = {}
    for cell in life:
        # set our defaults for cell neighbors
        fw, bw, up, dn = 1, -1, horizontal_boxes, -horizontal_boxes
        # set up our edge cases for cell neighbors
        if cell%horizontal_boxes == 0:  # means we are on left edge of grid
            bw = horizontal_boxes - 1

        if (cell+1)%horizontal_boxes == 0: # means we are on right edge of grid
            fw = -horizontal_boxes + 1

        if (cell-horizontal_boxes) < 0:  # means we are on bottom edge
            dn = (vertical_boxes*horizontal_boxes) - horizontal_boxes

        if (cell+horizontal_boxes) > ((vertical_boxes*horizontal_boxes) - 1):  # means we are on the top edge
            up = horizontal_boxes - ((vertical_boxes*horizontal_boxes) - cell) - cell

        # now we can count the neighbor score. Have 8 neighbors
        score = life[cell + fw] + life[cell + bw] + life[cell + up] + life[cell + dn] + life[cell + up + fw] + \
                life[cell + up + bw] + life[cell + dn + fw] + life[cell + dn + bw]
        if score < 2:
            new_life[cell] = 0
        if score == 2:
            new_life[cell] = life[cell]
        if score == 3:
            new_life[cell] = 1
        if score > 3:
            new_life[cell] = 0
    # print('from kill or create -     life is', life)
    # print('from kill or create - new_life is', new_life)
    return new_life


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    horizontal_boxes = 7
    vertical_boxes = 17
    box_size = 10
    main(horizontal_boxes, vertical_boxes, box_size)

