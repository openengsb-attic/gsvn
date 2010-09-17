from optparse   import OptionParser
from shlex      import split
from subprocess import Popen
from subprocess import PIPE

""" Command line interface for gsvn """

def parseArguments( args ):
	"""Parses list of string arguments. Returns an object with the converted arguments as fields."""

	# init parser
	usage = """gsvn googleDocsUsername googleDocsPassword svnUsername svnPassword
     googleDocsUsername  email address of the google user account
     googleDocsPassword  password of the google user account

     svnUsername         username for svn repo authentication
     svnPassword         password for svn repo authentication"""

	parser = OptionParser( prog = 'gsvn', usage = usage )

	parser.add_option(
		"-g", "--gDocsRoot", help="name of the root of the file tree to copy fetch from google docs, default is root folder",
		type = "string", action="store" )
	parser.add_option(
		"-s", "--svnRoot", help="path to directory into which the google doc file tree shall be copied into, default is current folder",
		type = "string", action="store" )
	
	parser.add_option( "-v", "--verbose", help="log messages during run of script", action="store_true", default=True )

	# parse args
	options, args = parser.parse_args( args )

	# check if there are the right number of arguments
	if len( args ) != 4:
		parser.print_help()
		print "error: gsvn requires exactly 4 arguments, %d given." % len( args )
		exit( 2 )
		
	# put mandatory arguments into options object for simplicity
	options.gDocsUsername = args[0]
	options.gDocsPassword = args[1]
	options.svnUsername   = args[2]
	options.svnPassword   = args[3]

	# dispose of parser
	parser.destroy()

	return options

def call( args ):
	""" Executes a program in the shell.
		
		args:		a string to execute in the shell or a sequence that is converted to a string for execution.
		
		Returns:	a 3-tuple of the programs return code, the programs standard output as string and it' error output
					as string.
					If the program has no standard output, the second part of the tuple will be None.
					If the program has no error output, the third part of the tuple will be None."""

	if type( args ) == str:
		args = split( args )

	process  = Popen( args, stdout=PIPE, stderr=PIPE )

	out, err = process.communicate()
	retCode  = process.poll()

	if len(out) == 0:
		out = None
	if len(err) == 0:
		err = None

	return retCode, out, err


