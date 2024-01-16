from lib.GUI import Root
from sys import argv


def main():

    largv = [str(arg).lower() for arg in argv]
    if '-gui' in largv:
        root = Root("./lib/settings.json")
        root.root.mainloop()
        return

    ## more CLI code can go here! most CLI functionality should be put in either utils.py or a new python file in lib ##


if __name__ == "__main__":
    main()
