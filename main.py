from lib.GUI import Root
from lib.settings import Settings, SettingsException
from lib.utils import generate_articles, generate_stock_report, generate_sentiment_report
from sys import argv


def main():

    largv = [str(arg).lower() for arg in argv]

    # This launches the GUI version of the program
    # SYNTAX: -gui
    if '-gui' in largv:
        root = Root('./lib/settings.json')
        root.root.mainloop()
        return  # no arguments after '-gui' are accepted

    settings_filename = "./lib/settings.json"
    for i, (arg, larg) in enumerate(zip(largv, argv)):

        # this loads a different settings file than the default ./lib/settings.json
        # SYNTAX: '-settings=directory/to/your/settings.json'
        if '-settings=' == larg[:10]:
            settings_filename = arg[10:]

        # this is a CLI way to change your settings
        # SYNTAX: '-settingsmod SettingName=NewSetting'
        elif '-settingsmod' == larg:
            try:
                # first, loads and instance of the settings to modify
                settings = Settings(settings_filename)

                # settingsmod is next argument after the '-settingsmod' argument
                settingsmod = argv[i+1]

                # this splits settingsmod at the first '='
                settingsmod_changed = False
                for j, ichar in enumerate(settingsmod):
                    if ichar == '=':
                        settingsmod = [settingsmod[:j], settingsmod[j+1:]]
                        settingsmod_changed = True
                        break
                # if no '=' was detected, the program raising an error
                if not settingsmod_changed:
                    raise SettingsException

                # if the user is attempting to change a setting that doesn't exist, raise an error
                if settingsmod[0] not in settings.s.keys():
                    raise SettingsException

                # the search terms are editted in the settings.json file or the GUI, not settingsmod
                if settingsmod[0] == 'SearchTerms':
                    raise SettingsException

                # Must account for settings that are not saved as strings
                # Therefore, they must be converted into their correct data type
                if settingsmod[0] in ['Running', 'NumArticles']:
                    # converts to bool
                    if settingsmod[0] == 'Running':
                        if settingsmod[1].lower() == 'true':
                            settingsmod[1] = True
                        elif settingsmod[1].lower() == 'false':
                            settingsmod[1] = False
                        else:
                            raise SettingsException

                    # converts to int
                    elif settingsmod[0] == 'NumArticles':
                        settingsmod[1] = int(settingsmod[1])

                # finally, we overwrite the current settings and save
                settings[settingsmod[0]] = settingsmod[1]
                settings.save()

            # if there is an exception in settingsmod, the program displays the error and continues
            except SettingsException:
                print("Invalid settings given for settingsmod. Ignoring and continuing")
                continue

        # these flags are the ones that add functionality to the CLI
        elif '-news' == larg:
            generate_articles(Settings(settings_filename))

        elif '-sentiment' == larg:
            generate_sentiment_report(Settings(settings_filename))

        elif '-sentimentonly' == larg:
            generate_sentiment_report(Settings(settings_filename), gen_articles=False)

        elif '-stock' == larg:
            generate_stock_report(Settings(settings_filename))


if __name__ == "__main__":
    main()
