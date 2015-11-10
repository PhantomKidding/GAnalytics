__author__ = 'cchen224'

import sys

def main(argv):
    with open(argv, 'wb') as f:
        f.write('json : client_secrets.json\n\n'
                'account : \n'
                'property : \n'
                'profile : \n'
                'start_date : \n'
                'end_date : \n'
                'filters : \n'
                'dimensions : \n'
                'metrics : \n'
                'segment : \n'
                'sort : \n'
                'sampling_level : \n'
                'max_results : \n'
                'start_index : \n\n'
                'output : result.csv')

if __name__ == '__main__':
    args = sys.argv
    if len(args) > 2:
        print 'Warning: more parameters than expected.'
    if args[1:]:
        main(args[1])
    else:
        main('setup.txt')