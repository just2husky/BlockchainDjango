def fun1(dict1):
    dict1 = dict1.copy()
    del dict1['a']
    print(dict1)

dict1={'a': 1, 'b': 2}
print(dict1)
fun1(dict1)
print(dict1)