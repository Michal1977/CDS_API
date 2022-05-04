import json


class CdLibrary:
    def __init__(self):
        try:
            with open("cds.json", "r") as f:
                self.cds = json.load(f)
        except FileNotFoundError:
            self.cds = []

    def all(self):
        return self.cds

    def get(self, id):
        cd = [cd for cd in self.all() if cd['id'] == id]
        if cd:
            return cd[0]
        return[]

    def create(self, data):
        self.cds.append(data)
        self.save_all()

    def search_by_name(self, match):
        result = [i for i in self.cds if match.upper() in i['name'].upper()]
        #list(filter(lambda item: item.name == match, self.cds))
        return result

    def save_all(self):
        with open("cds.json", "w") as f:
            json.dump(self.cds, f)

    def update(self, id, data):
        item = self.get(id)
        if item:
            index = self.cds.index(item)
            self.cds[index] = data
            self.save_all()
            return True
        return False

    def delete(self, id):
        cd = self.get(id)
        if cd:
            self.cds.remove(cd)
            self.save_all()
            return True
        return False


cds = CdLibrary()

