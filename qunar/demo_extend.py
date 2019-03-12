# coding=utf-8


class A(object):
    def __init__(self):
        a = 1
        b = '1234'


class B(A):
    def __init__(self):
        c = 'aa'

b_obj = B()
print b_obj.__init__()
