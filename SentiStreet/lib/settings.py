import json


class Settings:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.s = dict()
        self.load()
        if self.s == {}:
            print("Error: invalid or corrupted settings files detected. Please fix immediately...\nTerminating")
            exit()

    def __getitem__(self, item: str):
        return self.s[item]

    def __setitem__(self, key: str, value):
        self.s[key] = value

    def save(self):
        with open(self.filepath, 'w') as json_file:
            json.dump(self.s, json_file, indent=4)

    def load(self):
        try:
            with open(self.filepath, 'r') as file:
                self.s = json.load(file)
        except FileNotFoundError:
            return
        except json.JSONDecodeError:
            return

    def settingsmod(self, settingsmod: str):
        try:

            # this splits settingsmod at the first '='
            settingsmod_changed = False
            for j, ichar in enumerate(settingsmod):
                if ichar == '=':
                    settingsmod = [settingsmod[:j], settingsmod[j + 1:]]
                    settingsmod_changed = True
                    break
            # if no '=' was detected, the program raising an error
            if not settingsmod_changed:
                raise SettingsException

            # if the user is attempting to change a setting that doesn't exist, raise an error
            if settingsmod[0] not in self.s.keys():
                raise SettingsException

            # the search terms can only be edited in the settings.json file or the GUI, not with settingsmod
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
            self[settingsmod[0]] = settingsmod[1]
            self.save()
            return True

        except SettingsException:
            return False


class SettingsException(Exception):
    pass
