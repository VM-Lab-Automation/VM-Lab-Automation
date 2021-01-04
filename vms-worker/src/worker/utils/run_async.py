import threading


def run_async(f):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=f, args=args, kwargs=kwargs)
        thread.setDaemon(True)
        thread.start()
    return wrapper
