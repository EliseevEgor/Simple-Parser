class DataBase:
    def __init__(self, name):
        self.name = name
        self.companies_info = dict()

    def add(self, name, info):
        self.companies_info[name] = info

    def delete(self, name):
        if self.companies_info.get(name) is None:
            raise KeyError()
        else:
            del self.companies_info[name]

    def get(self, name):
        if self.companies_info.get(name) is None:
            raise KeyError()
        else:
            return self.companies_info.get(name)

    def size(self):
        return len(self.companies_info)

    def clear(self):
        self.companies_info.clear()
