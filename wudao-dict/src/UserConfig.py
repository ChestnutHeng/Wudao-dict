import json


class UserConfig:
    def __init__(self):
        self.conf_file = './user/conf.json'

    # dump config as json file
    def conf_dump(self, conf):
        with open(self.conf_file, "w+") as file:
            json.dump(conf, file, indent=4)

    # read config from json file
    def conf_read(self):
        try:
            with open(self.conf_file, "r") as file:
                conf = json.loads(file.read())
            return conf
        except:
            self.conf_dump({"short": False, "save": False})
