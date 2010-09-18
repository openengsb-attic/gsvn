from __future__ import print_function

from cli  import parseArguments
from docs import downloadDocs
from svn  import commitToRepo

def main( args ):
	# drop program name from cmd line args and parse them
	args = parseArguments( args[1:] )

	# download files from google docs
	downloadDocs( args.gDocsUsername, args.gDocsPassword, args.gDocsRoot, args.svnRoot )

	# commit to svn
	commitToRepo( args.svnUsername, args.svnPassword, args.svnRoot )

# if we this is run as a standalone script execute main
if __name__ == "__main__":
	from sys import argv

	main( argv )

