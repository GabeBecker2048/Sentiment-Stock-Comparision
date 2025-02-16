#from lib.GUI import Root
from lib.settings import Settings
from lib.utils import *
from sys import argv


def main():

    largv = [str(arg).lower() for arg in argv]

    # this loads a different settings file than the default ./lib/settings.json
    # SYNTAX: '-settings=directory/to/your/settings.json'
    settings_filename = './lib/settings.json'
    for i in range(len(largv)):
        if largv[i][:10] == '-settings=':
            settings_filename = argv[i][10:]

    # This detects if we are using the GUI or the non-GUI version
    # if '-nogui' is added, then this processes CLI commands
    # SYNTAX: -nogui
    # if '-nogui' not in largv:
    #     root = Root(settings_filename)
    #     root.root.mainloop()
    #     return  # no other arguments are accepted

    # ------------------------------------------
    # Everything below here only runs in the CLI
    # ------------------------------------------

    CLI_Settings = Settings(settings_filename)
    for i, (arg, larg) in enumerate(zip(largv, argv)):

        # this is a CLI way to change your settings
        # SYNTAX: '-settingsmod SettingName=NewSetting'
        if '-settingsmod' == larg:
            if not CLI_Settings.settingsmod(argv[i+1]):
                print("Invalid settingsmod argument given. The settings will not be changed")
            else:
                print(f"The settings at '{settings_filename}' have been adjusted! {argv[i+1]}")

        # these flags are the ones that add functionality to the CLI
        elif '-run' == larg:
            run_all(CLI_Settings)

        elif '-news' == larg:
            generate_articles(CLI_Settings)

        elif '-sentiment' == larg:
            generate_sentiment_report(CLI_Settings)

        elif '-sentimentonly' == larg:
            generate_sentiment_report(CLI_Settings, gen_articles=False)

        elif '-stock' == larg:
            generate_stock_report(CLI_Settings)


if __name__ == "__main__":
    main()
