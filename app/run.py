from app import create_app
import os


if __name__ == '__main__':
    create_app(testing=False).run()
