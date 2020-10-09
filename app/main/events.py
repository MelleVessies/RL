from flask_socketio import emit, send
import json
import time
from .. import socketio

############################
# IGNORE THIS FILE FOR NOW!!!!!!!!!!!!!!!!!
################################

class Worker(object):

    switch = False

    def __init__(self, socketio):
        """
        assign socketio object to emit
        """
        self.socketio = socketio
        self.switch = True

    def start(self):
        self.switch = True

    def do_work(self, id):
        """
        do work and emit message
        """
        generator = mosaic.create_mosaic_generator(id)
        while self.switch:
            ids = next(generator, None)
            if ids is None:
                self.switch = False
                break

            emit('mosaic_update', json.dumps(ids))
            time.sleep(0.02)

    def stop(self):
        """
        stop the loop
        """
        self.switch = False
        emit('clear_charts')


@socketio.on('get_mosaic')
def socket_get_mosaic(id):
    worker.start()
    socketio.start_background_task(target=worker.do_work(id))

@socketio.on('stop_mosaic')
def stop_mosaic():
    worker.stop()

@socketio.on('connect')
def test_connect():
    global worker
    worker = Worker(socketio)
    print("Connection succesful")