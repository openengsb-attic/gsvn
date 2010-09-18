from __future__ import print_function

from os                 import makedirs
from os.path            import exists
from gdata.service      import RequestError
from gdata.docs.service import DocsService, DocumentQuery

""" special categories from google docs that are not really folders.
	fetched from http://code.google.com/apis/documents/docs/3.0/reference.html
	TODO: update automatically"""
DOC_TYPES          = set(['document', 'folder', 'pdf', 'presentation', 'spreadsheet', 'form'])
DOC_STATES         = set(['starred', 'trashed', 'hidden', 'viewed', 'mine', 'private', 'shared-with-domain'])
SPECIAL_CATEGORIES = DOC_TYPES.union( DOC_STATES )
ROOT_FOLDER        = None

def downloadDocs( username, password, srcFolder, dstFolder ):
	client = GoogleClient( username, password )

	docs = client.getAllDocuments()

	startDoc = _getStartDoc( srcFolder, docs )

	_download( client, docs, dstFolder, startDoc )

def _download( client, allDocs, dst, doc ):
	newDst = client.saveTo( doc, dst )
	
	for child in _childrenOf( doc, allDocs ):
		_download( client, allDocs, newDst, child )

def _getStartDoc( name, allDocs ):
	if name == None:
		return None
	else:
		return allDocs[ allDocs.index( name ) ]

def _childrenOf( doc, allDocs ):
	""" return all entries from allDocs that are a child of doc. """

	return filter( lambda x: x.isChildOf( doc ), allDocs )

class GoogleClient(object):
	""" a wrapper for the google docs client that simplifies the few operations we need. """

	def __init__( self, username, password ):
		self.__client = DocsService()
		self.__client.ClientLogin( username, password )

	def getAllDocuments( self ):
		query = DocumentQuery()
		query['showfolders'] = 'true'

		docs = self.__client.Query( query.ToUri() ).entry

		return map( File, docs ) # wrap in File objects

	def saveTo( self, doc, dst ):
		"""Save a file to the file system. Returns the path the file was saved to."""

		# ignore root
		if doc == ROOT_FOLDER:
			return dst

		docPath = dst + '/' + doc.title

		try:
			if doc.isFolder:
				self.__createFolder( docPath )
			else:
				self.__client.Export( doc._File__doc, docPath )
		except RequestError as e:
			print( "Could not download file '" + doc.title + ", reason:", e.args[0]['reason'] )
		except Exception as e:
			print( "An exception occured while saving file " + doc.title + ":", type(e), e.args )

		return docPath

	@staticmethod
	def __createFolder( folder ):
		""" create a folder if it doesn't exist yet. """

		if not exists( folder ):
			makedirs( folder )

class File(object):
	""" a wrapper class that simplifies working with google docs objects """

	def __init__( self, googleDoc ):
		self.__doc     = googleDoc
	
		# extract parent folders, type info and status
		categoryNames     = map( lambda category: category.label, googleDoc.category )
		specials, folders = partition( lambda x: x in SPECIAL_CATEGORIES, categoryNames )

		docType = set(specials) - DOC_STATES

		self.type     = docType.pop() if len(docType) == 1 else None
		self.parents  = folders if len(folders) > 0 else [ROOT_FOLDER]

	@property
	def title( self ):
		return self.__doc.title.text

	@property
	def isFolder( self ):
		return self.type == 'folder'

	def isChildOf( self, folder ):
		return folder in self.parents

	def __eq__( self, that ):
		if that == None:
			return False		
		elif type(that) == str:
			return self.title == that
		else:
			return self.title == that.title
	
	def __repr__( self ):
		return "<" + ("Folder" if self.isFolder else "Document") + ": " + self.title + ">"

def partition( pred, list ):
	""" The partition function takes a predicate a list and returns the pair of lists of elements which do and
        do not satisfy the predicate, respectively."""

	true  = []
	false = []

	for i in list:
		if pred( i ):
			true.append( i )
		else:
			false.append( i )

	return true, false

