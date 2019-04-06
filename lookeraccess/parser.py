import yaml

class Config:

    def __init__(self, path):
        self.raw=self.read_from_path(path)
        self.groups = self.raw['groups']
        self.users = self.raw['users']
        self.roles = self.raw['roles']
        self.permissionsets = self.raw['permissionsets']
        self.modelsets = self.raw['modelsets']

    def __repr__(self):
        return "Config with {} users, {} groups, {} roles, {} permission sets and {} model sets.".format(
            len(self.users),
            len(self.groups),
            len(self.roles),
            len(self.permissionsets),
            len(self.modelsets)
            )


    def read_from_path(self, path):
        with open(path, 'r') as stream:
            try:
                config = yaml.load(stream)
                return config
            except yaml.YAMLError as exc:
                print(exc)

