from distutils.core import setup
import py2exe
import pgrep

copyright = " Programus"

setup(
    version = pgrep.ver,
    description = "A grep like command-line tool. \nIt gets paragraph result instead.", 
    name = "pgrep",
    console = ["pgrep.py", 
		{
		"script":"pgrep.py", 
		"icon_resources":[(1,"pgrep.ico")], 
		}], 
	data_files = [("", ["readme.txt", ]), ]

)

