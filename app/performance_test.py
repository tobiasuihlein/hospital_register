import time
from taipy import Gui

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

@timer
def run_app():
    page = "# Profiled Taipy Test 3"
    Gui(page).run(use_reloader=True)

if __name__ == "__main__":
    run_app()