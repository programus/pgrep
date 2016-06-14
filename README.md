# Pgrep
----
pgrep v1.00.x071127
by Programus (programus@gmail.com)
----

An open source and free command line grep like tool. 
It prints out the paragraphs which contains the pattern instead of lines. 

    Usage: pgrep.py [OPTION]... PATTERN [FILE] ...
    <If you run from source code> python pgrep.py [OPTION]... PATTERN [FILE] ...
    
    Search for PATTERN in each FILE or standard input and output a paragraph separated by separator. 
    Example: python pgrep.py -i 'hello world' menu.h main.c
    
    OPTIONS:
    -c, --count
    	Suppress normal output; instead print a count of matching lines for each input file.
    	With the -v, --invert-match option, count non-matching lines.
    -e, --regexp=PATTERN
    	Use pattern as the pattern; useful to protect patterns beginning with a -.
    -f, --file=FILE
    	Obtain patterns from file, one per line.  The empty file contains zero patterns, and therefore matches nothing.
    -h, --help
    	Print this help
    -i, --ignore-case
    	Ignore case distinctions in both the pattern and the input files.
    -l, --files-with-matches
    	Suppress normal output; instead print the name of each input file from which output would normally have been printed.
    	The scanning of every file will stop on the first match.
    -p, --separator=SEPARATOR
    	Specify a separator. The default separator is '\n\s*\n'. 
    -v, --invert-match
    	Invert the sense of matching, to select non-matching parts.
  