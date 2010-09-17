from __future__ import print_function

import cli

#####

def main( *args ):
	# drop program name from cmd line args and parse them
	args = cli.parseArguments( args[1:] )

class File:
	""" a wrapper class that simplifies working with google docs objects """

	def __init__( self, googleDoc ):
		self.__doc = googleDoc

	@property
	def title( self ):
		return self.__doc.title.text

	@property
	def isFolder( self ):
		return 'folder' in self.categories

	@property
	def categories( self ):
		return map( lambda category: category.label, self.__doc.category )

	def __repr__( self ):
		return "<" + ("Folder" if self.isFolder else "Document") + ": " + self.title + ">"
		
def getAllDocuments( email, password ):
	import gdata.docs.service

	client = gdata.docs.service.DocsService()
	client.ClientLogin( email, password )

	query = gdata.docs.service.DocumentQuery()
	query['showfolders'] = 'true'

	return client.Query( query.ToUri() ).entry

def getAllDocsInFolder( folder, docs ):
	return partition( lambda doc: folder in map( lambda c: c.label, doc.category ), docs )

def partition( pred, list ):
	true  = []
	false = []

	for i in list:
		if pred( i ):
			true.append( i )
		else:
			false.append( i )

	return true, false

# if we this is run as a standalone script execute main
if __name__ == "__main__":
	from sys import argv

	main( sys.argv )

