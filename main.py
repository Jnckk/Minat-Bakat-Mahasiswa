import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from src.controllers import ApplicationController


def main():
    try:
        app = ApplicationController()
        app.start_application()
    except KeyboardInterrupt:
        pass
    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    main()
