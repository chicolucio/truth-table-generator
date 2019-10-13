import argparse
import truths
import ast

def clielement():
    parser = argparse.ArgumentParser()
    parser.add_argument('variables',
                        help="List of variables e. g. \"['p', 'q']\"")
    parser.add_argument('-p', '--propositions',
                        help="List of propositions e. g. \"['p or q', 'p and q']\"")
    parser.add_argument('-i', '--ints', default='True',
                         help='True for 0 and 1; False for words')
    args = parser.parse_args()

    variables = ast.literal_eval(args.variables)
    ints = ast.literal_eval(args.ints)

    print()
    if args.propositions == None:
        propositions = []
        print(truths.Truths(variables, propositions, ints))
    else:
        propositions = ast.literal_eval(args.propositions)
        print(truths.Truths(variables, propositions, ints))
    print()

if __name__ == "__main__":
    clielement()
