import argparse
import faber
import os
import subprocess
def main():
    parser = argparse.ArgumentParser(prog='faber',
                                     description='faber demo package.')

    parser.add_argument('mode', type=str,
                        help='init the project')
    parser.add_argument('--type', default='base')
    parser.add_argument('--name', type=str, default='example_project')
    args = parser.parse_args()

    print(args)
    if args.mode == 'init':
        if args.type == 'base':
            copy_to_local(args.name)


def copy_to_local(name):
    dir_path = os.path.dirname(os.path.realpath(faber.__file__))
    copy_path = dir_path + '/example_project'
    print(copy_path)
    if os.path.exists(name):
        print('path exists.. overwrite?')
        overwriter = input('y or n')
        if overwriter != 'y':
            return
        else:
            subprocess.call(f'rm -r {name}', shell=True)
    subprocess.call(f'cp -r {copy_path} {name}', shell=True)
    return 0