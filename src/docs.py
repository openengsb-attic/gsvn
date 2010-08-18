import gdata.docs.service
import os
import os.path

class DocumentService(object):
	""" A simple wrapper around the google list data API for querying for files by name.
		An instance of this class corresponds to a google docs account.
	 """

	def __init__( self, email, password ):
		""" Creates a service object and logs into google Docs """

		# Create a client which will make HTTP requests with Google Docs server.
		self.__googleDocsClient = gdata.docs.service.DocsService()
		# Authenticate using your Google Docs email address and password.
		self.__googleDocsClient.ClientLogin( email, password )

	def getAllFiles( self ):
		""" Get a list of all files accessible by the user this service corresponds to. 

			returns	a list of google docs entry objects
		"""

		query = gdata.docs.service.DocumentQuery()
		query['showfolders'] = 'true'

		return self.__query( query )

	def getFile( self, name ):
		""" Query for a file by name.
			If no such file exists return None. 

			name	a string

			returns a google docs entry object

			TODO: do this by directly querying for the file by title.
					problem: we have to mangle the name to take care of special characters such as ?,|,{,},',"
		"""

		for file in self.getAllFiles():
			if file.title.text == name:
				return file
		
		# if we got here no file was found
		return None

	def getChildren( self, folder ):
		""" Get a list of all children of a folder. If the given file is not a folder an empty list is returned. 

			folder	a string
			
			returns a list of google docs entry objects
		"""
		
		query = gdata.docs.service.DocumentQuery()
		query.categories.append( self.__toName( folder ) )
		query['showfolders'] = 'true'

		return self.__query( query )

	def saveTo( self, doc, path ):
		docPath = path + '/' + doc.title.text

		if self.__isFolder( doc ):
			self.__createFolder( docPath )
			for file in self.getChildren( doc ):
				self.saveTo( file, docPath )
		else:
			self.__googleDocsClient.Download( doc, docPath )
		
	## HELPERS

	def __query( self, query ):
		""" Query for a Document List Feed and return the list of entries of that feed. """		

		return self.__googleDocsClient.Query( query.ToUri() ).entry

	@staticmethod
	def __isFolder( doc ):
		""" Check if a given entry is a folder. """

		return len( filter( lambda x: x.label == 'folder', doc.category ) ) >  0

	@staticmethod
	def __toName( obj ):
		""" iff obj is a string, just return it.
			otherwise return obj.title.text """

		if type(obj) == str:
			return obj
		else:
			return obj.title.text

	@staticmethod
	def __createFolder( folder ):
		""" create a folder if it doesn't exist yet. """

		if not os.path.exists( folder ):
			os.mkdir( folder )


