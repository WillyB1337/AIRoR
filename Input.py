import sys
import threading
import datetime

started = False
position = None
rotation = None
speed = None
lock = threading.Lock()
started = False


def init():
    thread = threading.Thread(target=read_stdin)
    thread.start()


def read_stdin():
    previous_position = [0.0, 0.0, 0.0]
    previous_timestamp = datetime.datetime.now()
    while True:
        try:
            for line in sys.stdin:
                if line[0:9] == "Position:":
                    timestamp = datetime.datetime.now()
                    stripped = line.replace('\x1b[0m\n', '').replace(' ', '')
                    data = stripped.split(':')
                    numeric_value = data[1].split(',')
                    global position
                    global rotation
                    global speed
                    lock.acquire()
                    position = [float(numeric_value[0]), float(numeric_value[1]), float(numeric_value[2])]
                    rotation = [float(numeric_value[3]), float(numeric_value[4]), float(numeric_value[5])]
                    global started
                    if started is False:
                        previous_position = position
                        speed = [0.0, 0.0, 0.0]
                        started = True
                    else:
                        duration = timestamp - previous_timestamp
                        #print("duration", duration.total_seconds())
                        for i in range(3):
                            speed[i] = (position[i] - previous_position[i]) / duration.total_seconds()

                        previous_timestamp = timestamp
                        previous_position = position
                    lock.release()
                    #print("pos", position)
                    #print("rot", rotation)
                    #print("spd", speed)

                #print(line, end='')
        except UnicodeDecodeError:
            print("UnicodeDecodeError exception")


def get_position():
    global lock
    global position
    lock.acquire()
    ret_position = position
    lock.release()

    return ret_position


def get_rotation():
    global lock
    global rotation
    lock.acquire()
    ret_rotation = rotation
    lock.release()

    return ret_rotation


def get_speed():
    global lock
    global speed
    lock.acquire()
    ret_speed = speed
    lock.release()

    return ret_speed


def is_started():
    global started
    return started