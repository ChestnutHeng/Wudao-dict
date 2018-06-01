import json


class UserConfig:
    def __init__(self):
        self.conf_file = './user/conf.json'
        self.conf = {}

    # dump config as json file
    def conf_dump(self):
        with open(self.conf_file, "w+") as file:
            json.dumps(self.conf,file , indent=4)

    # read config from json file
    def conf_read(self):
        try:
            with open(self.conf_file, "r") as file:
                self.conf = json.loads(file.read())
        except IOError as e:
            self.conf_dump()
        except json.JSONDecodeError as e:
            self.conf_dump()
