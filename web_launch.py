from flask import Flask
from threading import Thread
import time
process_run = True

app = Flask(__name__)

number_of_lines = 100


def print_lines():
    Thread(target=async_print2, args=(app, number_of_lines)).start()


def async_print2(app, number_of_lines):
    global process_run
    process_run = True
    for x in range(number_of_lines):
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