""" See https://docs.python.org/3/library/argparse.html for usage. """

def add_log_level(parser):
    parser.add_argument('-d', '--debug', dest='log_level',
                        action='store_const', const='DEBUG', default='INFO')
    parser.add_argument('-q', '--quiet', dest='log_level',
                        action='store_const', const='ERROR', default='INFO')
    return parser
