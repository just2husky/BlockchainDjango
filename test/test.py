import time
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


print(time.time())
print(time.localtime( time.time() ))
print(time.asctime( time.localtime(time.time()) ))
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )

print(type(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))

print(type(time.time()))