from flask import Flask
from threading import Thread
import time
process_run = True

app = Flask(__name__)


def print_lines():
    Thread(target=async_print2).start()


def async_print2():
    global process_run
    process_run = True
    for x in range(1000):
        if process_run is False:
            return
        print("Im running a process {}".format(x))
        time.sleep(0.5)


@app.route('/')
def front_page():
    print_lines()
    return 'hello world for test 2'


@app.route('/page2')
def page2():
    global process_run
    process_run = False
    return 'global changed'

if __name__ == '__main__':
    app.run()