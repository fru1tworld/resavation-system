import time
import threading

# 설정값
EPOCH = 1609459200000  
MACHINE_ID = 1         
SEQUENCE_MASK = 0xFFF  

lock = threading.Lock()
last_timestamp = -1
sequence = 0

def get_timestamp():
    return int(time.time() * 1000)

def wait_for_next_millis(current_timestamp):
    while True:
        ts = get_timestamp()
        if ts > current_timestamp:
            return ts

def generate_snowflake_id():
    global last_timestamp, sequence

    with lock:
        timestamp = get_timestamp()

        if timestamp == last_timestamp:
            sequence = (sequence + 1) & SEQUENCE_MASK
            if sequence == 0:
                timestamp = wait_for_next_millis(timestamp)
        else:
            sequence = 0

        last_timestamp = timestamp

        snowflake_id = ((timestamp - EPOCH) << 22) | (MACHINE_ID << 12) | sequence
        return snowflake_id
