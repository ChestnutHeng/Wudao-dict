import json


class UserConfig:
    def __init__(self):
        self.conf_file = './usr/conf.json'
        self.conf = {}

    # dump config as json file
    def conf_dump(self, conf):
        with open(self.conf_file, "w+") as file:
            file.write(json.dumps(self.conf, sort_keys=True, indent=4, separators=(',', ': ')))

    # read config from json file
    def conf_read(self):
        try:
            with open(self.conf_file, "r") as file:
                self.conf = json.loads(file.read())
        except IOError as e:
            self.conf_dump()
        except json.JSONDecodeError as e:
            self.conf_dump()
