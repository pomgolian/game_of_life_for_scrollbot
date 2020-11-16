from flask import Flask, render_template, url_for, request
from threading import Thread
import time
from game_of_life import Life, display_life, display_scroll_text, save_game, get_highest_score_game
from werkzeug.utils import redirect

# todo add dropdown list to select more apps
# todo save highest iterations score to HDD for persistance
# todo save initiation sequence for the highest iteration score to HDD and allow replay


app = Flask(__name__)

if 'process_status' not in globals():
    process_status = 'stopped'


if 'process_spawned' not in globals():
    process_spawned = False


def spawn_async_process(process_name, load_highest_score='No'):
    if process_name == 'game_of_life':
        Thread(target=gol(load_highest_score), args=()).start()


def gol(load_highest_score):
    global process_status
    global process_spawned
    process_spawned = True
    highest_iterations = 0
    while process_status == 'running': # process_run gets set to running from web page submit
        # the update_life method creates a new life sequence and returns repeating if sequence is repeating.
        # if we have a repeating sequence, quit current game, and start new game while process_run is true
        game = Life(17, 7) # create a new game with the size of the LED screen
        if load_highest_score == 'Yes':
            highest_iterations, game.life = get_highest_score_game()
        while game.update_life() == 'unique' and process_status == 'running':
            # keeps looping as long as no repeating patterns
            display_life(game.life) # send the current game to display on the LED screen
            time.sleep(.5) # leave the display for a split second before refreshing
        # display the stats for each game before starting a new game.
        if game.update_life() == 'repeating': # end of game, patterns are now repeating
            if game.iteration > highest_iterations:
                highest_iterations = game.iteration
                save_game(highest_iterations, game.initial_sequence)
            display_scroll_text('Current {} vs {}  '.format(game.iteration, highest_iterations), 10)
        time.sleep(1)
    process_spawned = False


@app.route('/')
def front_page():
    load_highest_score = request.args.get('load_highest_score', default='No')
    highest_iterations, life = get_highest_score_game()
    global process_status
    global process_spawned
    my_process = 'game_of_life'
    if process_spawned is False and process_status == 'running':
        spawn_async_process(my_process, load_highest_score)
    return render_template("web_run.html", process_status=process_status, highest_iterations=highest_iterations)


@app.route('/stop')
def stop():
    global process_status
    process_status = 'stopped'
    return redirect(url_for('front_page'))


@app.route('/start')
def start():
    global process_status
    process_status = 'running'
    return redirect(url_for('front_page', load_highest_score='No'))


@app.route('/start_high_score')
def start_high_score():
    global process_status
    process_status = 'running'
    return redirect(url_for('front_page', load_highest_score='Yes'))


if __name__ == '__main__':
    app.run(host='127.0.0.1')
