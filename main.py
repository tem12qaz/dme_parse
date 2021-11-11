from threading import Thread

from app import app
from parser import parse_cycle

if __name__ == '__main__':
    Thread(target=parse_cycle, args=()).start()
    app.run()
