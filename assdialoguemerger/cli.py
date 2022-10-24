"""
The command-line interface for assDialogueMerger
"""
import os
import glob
import argparse
from .assdialoguemerger import DialogueMerger, InputCountException


def directory(arg_value):
    """ Directory type to test if string is a valid directory """
    if not os.path.isdir(arg_value):
        raise argparse.ArgumentTypeError("not a valid directory")
    return arg_value


def main():
    """ Main Function """
    parser = argparse.ArgumentParser()
    parser.add_argument('-bf', '--base-folder', required=True, type=directory,
                        help='Directory path containing the base subtitle files')
    parser.add_argument('-df', '--dialogue-folder', required=True, type=directory,
                        help='Directory path containing the dialogue subtitle files')
    parser.add_argument('-dc', '--dialogue-changes', default=-1,
                        help='The maximum similarity between the base sub and dialogue\
                              sub dialogue for it to be added to the output file that\
                              contains a list of all overwritten dialogue. 1 = 100%%')
    parser.add_argument('-f', '--filter', default=None,
                        help='Regex for filtering the events (in both files), '
                             'see README for default value')
    # TODO: custom output formatting
    # parser.add_argument('-o', '--output', required = True,
    #                     help='''Output format string. %F0 = filename of 1st given input file,
    # 			        %I2+1 = index of file in directory with minimum of 2 digits and offset +1''')
    args = parser.parse_args()

    base_files = glob.glob(f"{args.base_folder}{os.path.sep}*.ass")
    dialogue_files = glob.glob(f"{args.dialogue_folder}{os.path.sep}*.ass")

    base_file_count = len(base_files)
    dialogue_file_count = len(dialogue_files)
    if base_file_count != dialogue_file_count:
        raise InputCountException(base_file_count, dialogue_file_count)

    dialogue_merger = DialogueMerger(float(args.dialogue_changes), args.filter)
    print()
    for i, (base_file, dialogue_file) in enumerate(zip(base_files, dialogue_files)):
        dialogue_merger.merge(base_file, dialogue_file,
                              f"{str(i+1).zfill(2)}.ass")


if __name__ == "__main__":
    main()
