from app import App
from editor.plugins import delete_temp
from atexit import register

if __name__ == "__main__":
    register(delete_temp)
    App()