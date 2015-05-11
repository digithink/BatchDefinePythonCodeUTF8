BatchDefinePythonCodeUTF8
====
A convenient script to batch place the magic comment(`# -*- encoding: utf-8 -*-`) into the specified Python source files, either as first or second line in the files.

Important
====
Backup your files or put the files into a source control repos before you execute the command.

How to use
====
Use shell script apply_utf8.py to batch place the magic comment. Use `-d` to specify the directory the script will search for the Python source files.

```
python apply_utf8.py -d DIR_OF_PYTHON_FILES
```

Notes
====
- The script will ignore the files which already have the magic comment. It can recognize  two pattern: `-*- coding: <encoding name> -*-` and `coding=<encoding name>`
- The script can recognize `#!/usr/bin/env python`. If this line exists, the magic comment will be inserted at the second line of the file.
- The script reads and writes data of the files in binary mode, your line breaks will be kept as they were.