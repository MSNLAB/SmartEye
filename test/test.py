import argparse

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group()
group.add_argument('-a', action='store_true')
group.add_argument('-b')
parser.add_argument('-c')


args = parser.parse_args()
print(args.a)
print(args.b)
print(args.c)

