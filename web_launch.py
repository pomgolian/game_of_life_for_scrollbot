from flask import Flask, render_template, url_for
from threading import Thread
import time
from game_of_life import Life, run_life

from werkzeug.utils import redirect

process_run = False

app = Flask(__name__)

my_process_arg = 100


def spawn_async_process():
    Thread(target=my_process, args=(app, my_process_arg)).start()


def my_process(app, my_arg):
    global process_run
    iterations = 0
    while process_run:
        life = 'unique'
        game = Life(17, 7)
        while life == 'unique':
            if game.update_life():  # if this is true, we have a repeating sequence so we can quit current game
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


@app.route('/')
def front_page():
    spawn_async_process()
    return render_template("web_run.html")


@app.route('/stop')
def stop():
    global process_run
    process_run = False
    return redirect(url_for('front_page'))


@app.route('/start')
def start():
    global process_run
    process_run = True
    return redirect(url_for('front_page'))


if __name__ == '__main__':
    app.run()
