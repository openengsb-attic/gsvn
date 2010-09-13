import cli
import docs

# parse command line arguments
args = cli.parseArguments()

# connect to google docs
googleDocs = docs.DocumentService( args.gDocsUsername, args.gDocsPassword )

# fetch documents
if args.gDocsRoot == None:
	files = googleDocs.getRoot()
else:
	files = googleDocs.getFile( args.gDocsRoot )

# save to repo
if args.svnRoot == None:
	googleDocs.saveTo( files, "." )
else:
	googleDocs.saveTo( files, args.svnRoot )

# commit to svn


