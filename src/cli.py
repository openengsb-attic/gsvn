from optparse   import OptionParser
from shlex      import split
from subprocess import Popen
from subprocess import PIPE, CalledProcessError

from docs import ROOT_FOLDER

""" Command line interface for gsvn """

def parseArguments( args ):
	"""Parses list of string arguments. Returns an object with the converted arguments as fields."""

	# init parser
	usage = """gsvn googleDocsUsername googleDocsPassword [svnUsername svnPassword]
     googleDocsUsername  email address of the google user account
     googleDocsPassword  password of the google user account

     svnUsername         username for svn repo authentication
     svnPassword         password for svn repo authentication"""

	parser = OptionParser( prog = 'gsvn', usage = usage )

	parser.add_option(
		"-g", "--gDocsRoot", help="name of the root of the file tree to copy fetch from google docs, default is root folder",
		type = "string", action="store", default=ROOT_FOLDER )
	parser.add_option(
		"-s", "--svnRoot", help="path to directory into which the google doc file tree shall be copied into, default is current folder",
		type = "string", action="store", default="." )
	
	parser.add_option( "-v", "--verbose", help="log messages during run of script", action="store_true", default=True )

	# parse args
	options, args = parser.parse_args( args )

	# check if there are the right number of arguments
	# put mandatory arguments into options object for simplicity
	if len( args ) == 4:
		options.gDocsUsername = args[0]
		options.gDocsPassword = args[1]
		options.svnUsername   = args[2]
		options.svnPassword   = args[3]
	elif len( args ) == 2:
		options.gDocsUsername = args[0]
		options.gDocsPassword = args[1]
		options.svnUsername   = None
		options.svnPassword   = None
	else:
		parser.print_help()
		print "error: gsvn requires exactly 2 or 4 arguments, %d given." % len( args )
		exit( 2 )

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

	# strings have to be split by whitespace for Popen
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

# Exception classes used by this module.
class GsvnCalledProcessError(CalledProcessError):
	"""This exception is raised when a process run by checkedCall() returns
	a non-zero exit status.  The exit status will be stored in the
	returncode attribute."""
	def __init__(self, returncode, cmd, errors ):
		self.returncode = returncode
		self.cmd        = cmd
		self.errors     = errors
	def __str__(self):
		str = "Command '%s' returned non-zero exit status %d" % (self.cmd, self.returncode)

		if self.errors:
			str += ": %s" % self.errors

		return str
		
def checkedCall( args ):
	""" Executes a program in the shell. If the program aborts with a non zero return code an exception is raised
		displaying the contents of the programs stderr
		
		args:		a string to execute in the shell or a sequence that is converted to a string for execution.
		
		Returns:	the called programs stdout output as string"""

	retCode, out, err = call( args )

	if retCode != 0:
		raise GsvnCalledProcessError( retCode, args, err )
		
	return out


