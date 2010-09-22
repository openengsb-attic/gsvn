from __future__ import print_function

from cli import checkedCall

def commitToRepo( folder, username=None, password=None ):
	"""Commits everything in folder to its repo. Files that are new are added.
       If username or password are present they will be used in the svn requests.
       Files with conflicts will not be added."""

	output = checkedCall( "svn status %s %s" % (_usernameAndPasswordToString( username, password ),folder) )

	for line in output.splitlines():
		checkAndAdd( username, password, line )

	# commit changes
	checkedCall( "svn commit %s %s -m 'automatic commit by gsvn tool'" % (_usernameAndPasswordToString( username, password ),folder) )

def checkAndAdd( username, password, line ):
	"""Check svn status of file and add it if necessary"""

	status = line[:8]
	file   = line[8:] # file name starts at 8th character of line
	
	try:
		checkSvnStatus( status, file )
		addFile( status, username, password, file )
	except Exception as e:
		print( e )	

def checkSvnStatus( status, file ):
	""" Check svn status of file:
		The first seven columns in the output are each one character wide: """

	# check status codes
	try:
		checkAddedDeletedChanged( status[0] )
		checkFileOrDirectoryProperties( status[1] )
		checkWorkingCopyLock( status[2] )
		checkScheduledHistoryWithCommit( status[3] )
		checkIsFileSwitchedOrExternal( status[4] )
		checkRepositoryLock( status[5] )
		checkForTreeConflict( status[6] )
	except Exception as e:
		raise Exception( "Could not commit file %s: %s" % (file, e) )

def addFile( status, username, password, file ):
	"""Add file to svn working copy. """

	# we need to escape whitespace in file names for the shell
	file = file.replace(' ',  '\ ')
	file = file.replace('\t', '\\t')
	file = file.replace('\n', '\\n')

	if status[0] == '?':
		checkedCall( "svn add %s %s" % (_usernameAndPasswordToString( username, password ), file) )

def checkAddedDeletedChanged( mode ):
	"""First column: Says if item was added, deleted, or otherwise changed
      ' ' no modifications
      'A' Added
      'C' Conflicted
      'D' Deleted
      'I' Ignored
      'M' Modified
      'R' Replaced
      'X' an unversioned directory created by an externals definition
      '?' item is not under version control
      '!' item is missing (removed by non-svn command) or incomplete
      '~' versioned item obstructed by some item of a different kind"""
	if ' ' == mode:
		pass # fine by me
	elif 'A' == mode:
		pass # fine by me
	elif 'C' == mode:
		raise Exception( "file has conflicts" )
	elif 'D' == mode:
		pass # fine by me
	elif 'I' == mode:
		pass # fine by me
	elif 'M' == mode:
		pass # fine by me
	elif 'R' == mode:
		pass # fine by me
	elif 'X' == mode:
		pass # fine by me
	elif '?' == mode:
		pass # fine by me
	elif '!' == mode:
		pass # fine by me
	elif '~' == mode:
		raise Exception( "versioned item obstructed by some item of a different kind" )
	else:
		raise Exception( "illegal status code in first column: %s" % mode )

def checkFileOrDirectoryProperties( mode ):
	"""Second column: Modifications of a file's or directory's properties
      ' ' no modifications
      'C' Conflicted
      'M' Modified"""
	#ignore this for now
	pass

def checkWorkingCopyLock( mode ):
	"""Third column: Whether the working copy directory is locked
      ' ' not locked
      'L' locked"""
	#ignore this for now
	pass

def checkScheduledHistoryWithCommit( mode ):
	"""Fourth column: Scheduled commit will contain addition-with-history
      ' ' no history scheduled with commit
      '+' history scheduled with commit"""
	#ignore this for now
	pass

def checkIsFileSwitchedOrExternal( mode ):
	"""Fifth column: Whether the item is switched or a file external
      ' ' normal
      'S' the item has a Switched URL relative to the parent
      'X' a versioned file created by an eXternals definition"""
	#ignore this for now
	pass

def checkRepositoryLock( mode ):
	"""Sixth column: Repository lock token
      (without -u)
      ' ' no lock token
      'K' lock token present
      (with -u)
      ' ' not locked in repository, no lock token
      'K' locked in repository, lock toKen present
      'O' locked in repository, lock token in some Other working copy
      'T' locked in repository, lock token present but sTolen
      'B' not locked in repository, lock token present but Broken"""
	#ignore this for now
	pass

def checkForTreeConflict( mode ):
	"""Seventh column: Whether the item is the victim of a tree conflict
      ' ' normal
      'C' tree-Conflicted
    If the item is a tree conflict victim, an additional line is printed
    after the item's status line, explaining the nature of the conflict."""
	#ignore this for now
	pass

def _usernameAndPasswordToString( username, password ):
	""" A helper that turns a username and/or password into svn --username/--password options.
		if username or password are None or empty strings they are simply ignored"""
		
	str = ""

	if username:
		str += " --username %s" % username
	if password:
		str += " --password %s" % password

	return str

