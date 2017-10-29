
def test(param):
    if 1 == param:
        return 1
    else:
        return 1, 2


a = test(1)
print(a)
b, c = test(2)
print(b)
print(c)

a = {'a': 1, 'b': 2}
b = {'b': 4, 'c': 3}
a.update(b)
print(a)