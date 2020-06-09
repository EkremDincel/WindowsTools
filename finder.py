import os
from os.path import join
import sys

class All():
    def __contains__(self, other):
        return True
    def __repr__(self):
        return "All()"

def scan(targets = (), directory = None, *, regex = False, extensions = All(), encoding = "utf-8", read_mode = "r", recursion_depth = None, raise_decode_erros = False, caseless = False):
    if recursion_depth is not None:
        _recursion = sys.getrecursionlimit()
        sys.setrecursionlimit(recursion_depth)
    try:
        if regex:
            import re
            targets = tuple(re.compile(i) for i in targets)
        elif caseless:
            for i, j in enumerate(targets):
                targets[i] = j.lower()
        if directory is None:
            directory = os.getcwd()
        if "b" in read_mode:
            encoding = None
        l = []
        scan_util(directory, targets, regex, extensions, encoding, read_mode, raise_decode_erros, caseless, l)
        return l
    except:
        raise
    finally:
        if recursion_depth is not None:
            sys.setrecursionlimit(_recursion)
            

def scan_util(directory, targets, regex, extensions, encoding, read_mode, raise_decode_erros, caseless, return_list):
##    global file
##    global d
##    d = directory
    if not os.path.exists(directory): return # ???
    for file in os.listdir(directory):
        full_path = join(directory, file)
        if os.path.isfile(full_path):
            _, extension = os.path.splitext(file)
            if extension in extensions:
                try:
                    with open(full_path, read_mode, encoding = encoding) as f:
                        data = f.read()
                except UnicodeError:
                    if raise_decode_erros:
                        raise
                else:
                    if caseless:
                        data = data.lower()
                    if regex:
                        for re in targets:
                            if re.search(data) is None:
                                break
                        else:
                            return_list.append(full_path) 
                    else:
                        for string in targets:
                            if string not in data:
                                break
                        else:
                            return_list.append(full_path)
                    del data
        else:
            scan_util(join(directory, file), targets, regex, extensions, encoding, read_mode, raise_decode_erros, caseless, return_list)

