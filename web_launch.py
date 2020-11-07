from flask import Flask, render_template, url_for
from threading import Thread
import time

from werkzeug.utils import redirect

process_run = False

app = Flask(__name__)

my_process_arg = 100


def spawn_async_process():
    Thread(target=my_process, args=(app, my_process_arg)).start()


def my_process(app, my_arg):
    global process_run
    for x in range(my_arg):
        if process_run is False:
            return
        print("Im running a process {}".format(x))
        time.sleep(0.5)


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