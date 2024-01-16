from lib.GUI import Root
from sys import argv


def main():

    if '-gui' in argv:
        root = Root("./lib/settings.json")
        root.root.mainloop()
        return

    ## more CLI code can go here! most CLI functionality should be put in either utils.py or a new python file in lib ##


if __name__ == "__main__":
    main()
