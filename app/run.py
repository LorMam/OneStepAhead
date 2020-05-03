from app import create_app
import os


dir = os.path.abspath(__file__)
os.chdir(dir + "/..")
print(os.getcwd())


if __name__ == '__main__':
    create_app(testing=False).run()
