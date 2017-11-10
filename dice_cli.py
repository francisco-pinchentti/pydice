import argparse
import sys

from dice_parser import check_string_format, build_named_dice_collection

EXIT_CODES_INVALID_COUNT = 1
EXIT_CODES_INVALID_FORMAT = 2

def main(arguments):
    if check_string_format(arguments.expression):
        if arguments.count and arguments.count < 1 or (arguments.count == 0):
            print >> sys.stderr, 'Count argument must be >= 1'
            exit(EXIT_CODES_INVALID_COUNT)
        name = arguments.name if arguments.name else ''
        total_times_to_run = arguments.count if arguments.count else 1
        ndb = build_named_dice_collection(name, arguments.expression)
        results = []
        for i in range(0, total_times_to_run):
            results.append(ndb.roll())
        if arguments.verbose == 1:
            print ndb.get_print_string(total_times_to_run, arguments.average)
        if arguments.verbose == 0:
            print results
        exit(0)
    else:
        print 'Invalid format for given expression'
        exit(EXIT_CODES_INVALID_FORMAT)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'expression',
        help='a dice roll expression such as 2d6+3 or 1d8-1d2+2',
        type=str)
    parser.add_argument(
        "-n",
        "--name",
        help='expression name to use while logging',
        type=str)
    parser.add_argument(
        "-c",
        "--count",
        help='ammount of times to roll (defaults to 1)',
        type=int)
    avg_parser = parser.add_mutually_exclusive_group(required=False)
    avg_parser.add_argument('-avg', '--average', dest='average', action='store_true')
    avg_parser.add_argument('-no-avg', '--no-average', dest='average', action='store_false')
    parser.set_defaults(average=False)
    parser.add_argument(
        "-v",
        "--verbose",
        type=int,
        help='increase output verbosity, may be 0 or 1 (default)')
    parser.set_defaults(verbose=1)
    main(parser.parse_args())
