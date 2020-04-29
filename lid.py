#!/usr/bin/env python
import os
import argparse
from argparse import ArgumentTypeError as err
import tqdm

class PathType(object):
    def __init__(self, exists=True, type='file', dash_ok=True):
        '''exists:
                True: a path that does exist
                False: a path that does not exist, in a valid parent directory
                None: don't care
           type: file, dir, symlink, None, or a function returning True for valid paths
                None: don't care
           dash_ok: whether to allow "-" as stdin/stdout'''

        assert exists in (True, False, None)
        assert type in ('file','dir','symlink',None) or hasattr(type,'__call__')

        self._exists = exists
        self._type = type
        self._dash_ok = dash_ok

    def __call__(self, string):
        if string=='-':
            # the special argument "-" means sys.std{in,out}
            if self._type == 'dir':
                raise err('standard input/output (-) not allowed as directory path')
            elif self._type == 'symlink':
                raise err('standard input/output (-) not allowed as symlink path')
            elif not self._dash_ok:
                raise err('standard input/output (-) not allowed')
        else:
            e = os.path.exists(string)
            if self._exists==True:
                if not e:
                    raise err("path does not exist: '%s'" % string)

                if self._type is None:
                    pass
                elif self._type=='file':
                    if not os.path.isfile(string):
                        raise err("path is not a file: '%s'" % string)
                elif self._type=='symlink':
                    if not os.path.symlink(string):
                        raise err("path is not a symlink: '%s'" % string)
                elif self._type=='dir':
                    if not os.path.isdir(string):
                        raise err("path is not a directory: '%s'" % string)
                elif not self._type(string):
                    raise err("path not valid: '%s'" % string)
            else:
                if self._exists==False and e:
                    raise err("path exists: '%s'" % string)

                p = os.path.dirname(os.path.normpath(string)) or '.'
                if not os.path.isdir(p):
                    raise err("parent path is not a directory: '%s'" % p)
                elif not os.path.exists(p):
                    raise err("parent directory does not exist: '%s'" % p)

        return string

# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-v", "--verbose", action='store_true', help="Show file name with number of lines")
ap.add_argument("directory", nargs=1, type=PathType(exists=True, type='dir'), help="Direcory to execute command")
args = vars(ap.parse_args())

# if args["directory"] {
#     directoryToExecute = args["directory"]
# }
directoryToExecute = args["directory"]

'''
    For the given path, get the List of all files in the directory tree 
'''
def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(os.path.abspath(dirName))
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles
def main():
    totalNumberOfLines = 0
    directoryToExecute = ""
    all_files = getListOfFiles(directoryToExecute)
    for each_file in tqdm.tqdm(all_files):
        file = open(each_file, "r", encoding='latin-1')
        # file.encode('utf-8')
        number_of_lines = 0
        number_of_words = 0
        number_of_characters = 0
        for line in file:
          line = line.strip("\n")
          words = line.split()
          number_of_lines += 1
          number_of_words += len(words)
          number_of_characters += len(line)
        file.close()
        totalNumberOfLines += number_of_lines
        if args["verbose"]:
            print(f"File: {each_file}, lines: {number_of_lines}, words: {number_of_words}, characters: {number_of_characters}.")
    niceInt = ""
    totalNumberOfLinesArray = [int(i) for i in str(totalNumberOfLines)][::-1]
    for index in range(len(totalNumberOfLinesArray)):
        if index % 3 == 0 and index != 0:
            niceInt = f'{totalNumberOfLinesArray[index]},{niceInt}'
        else:
            niceInt = f'{totalNumberOfLinesArray[index]}{niceInt}'
    print(f'There are exactly {niceInt} lines in this directory')

if __name__ == "__main__":
    main()