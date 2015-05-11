#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
apply_utf8.py
A script to insert UTF-8 encoding header

Created by Xia on 2015-04-07.

- Insert `ENCODING_LINE` at the first line (or second line) of the file.
- Ignore if `ENCODING_LINE` already exists, supports two formats:
  #. -*- coding: <encoding name> -*-
  #. coding=<encoding name>
- Recoginze `#!/usr/bin/env python`. If this line exists, `ENCODING_LINE` will
  be inserted at the second line of the file.
"""

import os
import re
import sys
import getopt

help_message = '''
[SAMPLE]
./apply_utf8.py -d DIR_OF_PYTHON_FILES
'''   
class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


ENCODING_REGEX = re.compile('coding[:=]\s*([-\w.]+)')
ENCODING_LINE = '# -*- encoding: utf-8 -*-\n'

def is_encoding_line(str):
    """
    # coding=<encoding name>
    # -*- coding: <encoding name> -*-

    The first or second line must match the regular
    expression "coding[:=]\s*([-\w.]+)"
    """
    match = ENCODING_REGEX.search(str)
    if match:
        return True
    return False
    
def apply_utf8_for_file(file_path):
    """
    Insert missing `# -*- encoding: utf-8 -*-`

    To define a source code encoding, a magic comment must
    be placed into the source files either as first or second
    line in the file
    
    https://www.python.org/dev/peps/pep-0263/
    
    Return: 0 (untouched)
            1 (inserted)
    """
    fp = open(file_path, 'r')
    count = 0
    line1 = None
    line2 = None
    for line in fp:
        if count == 0:
            line1 = line
        elif count == 1:
            line2 = line
        else:
            break
        count += 1
    fp.close()
    found = False
    if line1 and is_encoding_line(line1):
        found = True
    elif line2 and is_encoding_line(line2):
        found = True
    else:
        pass
    if found:
        return 0
    
    index = 0
    if line1 and line1.startswith('#!'):
        index = 1
    fp = open(file_path, 'rb')
    if index == 0:
        data = fp.read()
        fp.close()
        fp = open(file_path, 'wb')
        fp.write(ENCODING_LINE)
        fp.write(data)
    elif index == 1:
        l = fp.readline()
        data = fp.read()
        fp.close()
        fp = open(file_path, 'wb')
        fp.write(l)
        fp.write(ENCODING_LINE)
        fp.write(data)
    else:
        pass
    return 1

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hd:", ["help", "dir="])
        except getopt.error, msg:
            raise Usage(msg)
        
        dir_path = None
                
        # option processing
        for option, value in opts:
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-d", "--dir"):
                dir_path = value
        
        if not dir_path:
            raise Usage(help_message)
            
        untouched_count = 0
        inserted_count = 0
        for dirname, dirnames, filenames in os.walk(dir_path):
            for filename in filenames:
                name, ext = os.path.splitext(filename)
                if ext != '.py':
                    continue
                path = os.path.join(dirname, filename)
                result = apply_utf8_for_file(path)
                if 0 == result:
                    print('[-]%s' % path)
                    untouched_count += 1
                elif 1 == result:
                    print('[+]%s' % path)
                    inserted_count += 1
                else:
                    pass
        print '\r\n====\r\nINSERTED: %d, UNTOUCHED: %d' % (inserted_count, untouched_count)
                
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2

    

    
if __name__ == "__main__":
    sys.exit(main())
