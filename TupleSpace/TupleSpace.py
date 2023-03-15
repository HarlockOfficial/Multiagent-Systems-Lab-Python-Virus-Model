
class TupleSpace:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(TupleSpace, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.tuples = []
        self.unpublished = []

    def out(self, entry: tuple):
        t = self.__take_unpublished(entry)
        if t is not None:
            self.tuples.append(t)
        else:
            self.tuples.append(entry)

    def get(self, entry: tuple):
        for t in self.tuples:
            if t[0] == entry[0]:
                return t
        return None

    def __take_unpublished(self, entry: tuple):
        for t in self.unpublished:
            if t[0] == entry[0]:
                self.unpublished.remove(t)
                return t
        return None

    def take(self, entry: tuple):
        for t in self.tuples:
            if t[0] == entry[0]:
                self.tuples.remove(t)
                return t
        return None

    def eval(self, entry: tuple):
        self.unpublished.append(entry)
