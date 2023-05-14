import logging

class MyHandler(logging.Handler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
    
    def emit(self, record):
        log_message = self.format(record)
        self.callback(log_message)

class CallBackLogger(logging.Logger):

    def __init__(self, name: str, callback, level):
        super().__init__(name, level)
        handler = MyHandler(callback)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s - %(message)s')
        handler.setFormatter(formatter)
        self.addHandler(handler)

def callback(log):
    print(log)


# usage logger = CallBackLogger(__name__, callback, logging.CRITICAL)

