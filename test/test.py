# import argparse
#
# parser = argparse.ArgumentParser()
#
# group = parser.add_mutually_exclusive_group()
# group.add_argument('-a', action='store_true')
# group.add_argument('-b')
# parser.add_argument('-c')
#
#
# args = parser.parse_args()
# print(args.a)
# print(args.b)
# print(args.c)


# class Test:
#     def __init__(self):
#         self.i = 0
#         self.j = 1
#         self.policy_set = {"a": self.a, "b": self.b}
#
#     def a(self):
#         print(self.i)
#
#     def b(self):
#         print(self.j)
#
#     def c(self, choice):
#         self.policy_set[choice]()
#
#
# test = Test()
# test.c('b')

class Test:
    def __init__(self):
        self.i = 100


class B:
    def __init__(self, a):
        self.a = a

    def p(self):
        self.a.i += 1


test = Test()
b = B(test)
b.p()

print(test.i)
