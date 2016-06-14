#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: Programus (programus@gmail.com)

import getopt, re, sys, os        

ver = "1.00.x071127"
C_FLAG = 1
I_FLAG = 1 << 1
L_FLAG = 1 << 2
V_FLAG = 1 << 3

argdict = {
        'h':('help',
             '-h, --help\n\tPrint this help',
             None),
        '-help':'h',
        
        'p:':('separator=',
              '-p, --separator=SEPARATOR\n\tSpecify a separator. The default separator is \'\\n\\s*\\n\'. ',
              lambda info, opt: ('separator', opt[1])),
        '-separator:': 'p:',
        
        'c':('count',
             '-c, --count\n\tSuppress normal output; instead print a count of matching lines for each input file.\n\tWith the -v, --invert-match option, count non-matching lines.',
             lambda info, opt: ('flag', info['flag'] | C_FLAG)),
        '-count':'c',
        
        'e:':('regexp=',
             '-e, --regexp=PATTERN\n\tUse pattern as the pattern; useful to protect patterns beginning with a -.',
              lambda info, opt: ('pattern', opt[1])),
        '-regexp:':'e:',
        
        'f:':('file=',
             '-f, --file=FILE\n\tObtain patterns from file, one per line.  The empty file contains zero patterns, and therefore matches nothing.',
              lambda info, opt: ('pattern', file(opt[1]).read())),
        '-file:':'f:',
        
        'i':('ignore-case',
             '-i, --ignore-case\n\tIgnore case distinctions in both the pattern and the input files.',
             lambda info, opt: ('flag', info['flag'] | I_FLAG)),
        '-ignore-case':'i',
        
        'l':('files-with-matches',
             '-l, --files-with-matches\n\tSuppress normal output; instead print the name of each input file from which output would normally have been printed.\n\tThe scanning of every file will stop on the first match.',
             lambda info, opt: ('flag', info['flag'] | L_FLAG)),
        '-files-with-matches':'l',
        
        'v':('invert-match',
             '-v, --invert-match\n\tInvert the sense of matching, to select non-matching parts.',
             lambda info, opt: ('flag', info['flag'] | V_FLAG)),
        '-invert-match':'v', 
        }

class NoEnoughArgumentsError(Exception):
    def __init__(self):
        Exception.__init__(self)
    def __str__(self):
        return 'No enough argument.'

def getsearchinfo(argv):
    shortoptstr = ''
    longoptstr = []
    for key, value in argdict.items():
        if not key.startswith('-'):
            shortoptstr += key
            longoptstr.append(value[0])
    opts, args = getopt.getopt(argv, shortoptstr, longoptstr)
    if not args and not opts:
        usage()
        sys.exit(1)

    # init information for searching. 
    info = {'pattern': None, 'separator': r'\n\s*\n', 'flag': 0, 'files': [sys.stdin]}
    # deal all options
    for opt in opts:
        k = opt[0][1:]
        if len(opt) > 1 and opt[1]:
            k += ':'
        t = argdict[k]
        if type(t) is tuple:
            func = t[2]
        else:
            func = argdict[t][2]
        if func is None:
            return None
        result = func(info, opt)
        info[result[0]] = result[1]

    try:
        if info['pattern']:
            files = args
        else:
            info['pattern'] = args[0]
            files = args[1:]
    except Exception:
        raise NoEnoughArgumentsError
    if files:
        info['files'] = [file(f) for f in files]
    
    return info

def search(info):
    count = 0
    flag = info['flag']
    for file in info['files']:
        try:
            try:
                parts = re.split(info['separator'], file.read())
                reflags = re.UNICODE | re.MULTILINE
                if flag & I_FLAG:
                    reflags |= re.IGNORECASE
                try:
                    pattern = re.compile(info['pattern'], reflags)
                    for part in parts:
                        if pattern.search(part):
                            if not flag & V_FLAG:
                                if flag & L_FLAG:
                                    print file.name
                                    print
                                    break
                                elif flag & C_FLAG:
                                    count += 1
                                else:
                                    print part
                                    print
                        elif flag & V_FLAG:
                            if flag & L_FLAG:
                                print file.name
                                print
                                break
                            elif flag & C_FLAG:
                                count += 1
                            else:
                                print part
                                print
                except re.error, e:
                    print 'Illegal regexp in pattern: %s' % str(e)
                    return
            except IOError, e:
                print '%s: \'%s\'' % (e.strerror, e.filename)
                return
            except re.error, e:
                print 'Illegal regexp in separator: %s' % str(e)
                return
        finally:
            file.close()
    if flag & C_FLAG and not flag & L_FLAG:
        print count

def main(argv):
    try:
        info = getsearchinfo(argv)
    except NoEnoughArgumentsError, e:
        print e
        usage()
    except IOError, e:
        print '%s: \'%s\'' % (e.strerror, e.filename)
    except getopt.GetoptError, e:
        print e
        usage()
    else:
        if info is None:
            usage()
        else:
            search(info)

def usage():
    print '''
------------------------------------
pgrep v''' + ver + '''
by Programus (programus@gmail.com)
------------------------------------
An open source and free command line grep like tool. 
It prints out the paragraphs which contains the pattern instead of lines. 

Usage: ''' + os.path.basename(sys.argv[0]) + ''' [OPTION]... PATTERN [FILE] ...
<If you run from source code> python ''' + os.path.basename(sys.argv[0]) + ''' [OPTION]... PATTERN [FILE] ...

Search for PATTERN in each FILE or standard input and output a paragraph separated by separator. 
Example: python pgrep.py -i 'hello world' menu.h main.c

OPTIONS:'''
    helps = [value[1] for value in argdict.values() if type(value) is tuple]
    helps.sort()
    print '\n'.join(helps)

if __name__ == '__main__':
    main(sys.argv[1:])
