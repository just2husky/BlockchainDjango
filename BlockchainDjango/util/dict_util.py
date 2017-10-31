class Struct:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    # def update_dict(self, **entries):
    #     self.__dict__.update(entries)

args = {'a': 1, 'b': 2}
s = Struct(**args)
print(type(s))
print(s.a)
print(s.b)