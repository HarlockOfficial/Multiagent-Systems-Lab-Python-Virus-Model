
class TupleSpace:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(TupleSpace, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.tuples = []
        self.unpublished = []

    def out(self, entry):
        t = self.__take_unpublished(entry)
        if t is not None:
            self.tuples.append(t)
        else:
            self.tuples.append(entry)

    def get(self, entry):
        for t in self.tuples:
            if t == entry:
                return t
        return None

    def __take_unpublished(self, entry):
        for t in self.unpublished:
            if t == entry:
                self.unpublished.remove(t)
                return t
        return None

    def take(self, entry):
        for t in self.tuples:
            if t == entry:
                self.tuples.remove(t)
                return t
        return None

    def eval(self, entry):
        self.unpublished.append(entry)
