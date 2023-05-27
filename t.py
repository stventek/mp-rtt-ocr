import tkinter as tk
import threading
import time
import signal
import os

class TaskThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._cancel = threading.Event()

    def cancel(self):
        self._cancel.set()

    def run(self):
        # Register the signal handler
        signal.signal(signal.SIGALRM, self._signal_handler)

        # Set an alarm to send the signal after 5 seconds
        signal.alarm(5)

        # Perform the task
        try:
            for i in range(1, 6):
                print("Task running...")
                time.sleep(1)
        except Exception as e:
            print("Task interrupted:", e)

        print("Task completed.")

    def _signal_handler(self, signum, frame):
        raise RuntimeError("Task interrupted by signal.")

def create_task():
    global current_task
    if current_task and current_task.is_alive():
        os.kill(os.getpid(), signal.SIGALRM)
    current_task = TaskThread()
    current_task.start()

current_task = None

root = tk.Tk()

button = tk.Button(root, text="Create Task", command=create_task)
button.pack()

root.mainloop()
