import argparse


def p(s):
    for i in s:
        print(i)
    print(len(s))


c = 0
parser = argparse.ArgumentParser(description='description')

parser.add_argument('-c',
                    action='store',
                    dest='d')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args)
