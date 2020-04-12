class Subject:
    OBS = []

    def add_ob(self, ob):
        self.OBS.append(ob)

    def remove_ob(self, ob):
        self.OBS.remove(ob)

    def notify(self, data):
        for ob in self.OBS:
            ob.update(data)