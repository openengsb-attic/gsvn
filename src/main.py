import sys
import docs

googleUsername = sys.argv[1]
googlePassword = sys.argv[2]
googleRootPath = sys.argv[3]

svnUsername    = ''
svnPassword    = ''
svnRootPath    = sys.argv[4]

googleDocs = docs.DocumentService( googleUsername, googlePassword )

googleDocs.saveTo( googleDocs.getFile( googleRootPath ), svnRootPath )


