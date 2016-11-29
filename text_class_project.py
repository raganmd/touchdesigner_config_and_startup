# Author | Matthew Ragan

import socket
import json
import os

target_file		= project.folder + '/{file}'
missing_file	= '''{file_name} is missing
Check your project directory to make sure 
you have all the appropriate files'''
project			= op.Project1

class Config:
	'''
	The Config class is used for setting up a project on start.

	There are various pieces of the start up process that require a
	high degree of configuration - especially in multi-server
	configurations. Doing this meaningfully is an important consideration
	in a large project. The Config class at the root of a project is 
	intended to faciltate this process and ensure seamless start up.

	This requires an additional system configuration file in the case
	of work at Obscura this most often looks like a JSON object with
	the various configuration information. In this project that
	file can be found here:

	touchdesigner_config_and_startup/data/system.json
	
	This file is used in conjunction with another machine
	configue file that specifies the id / role of this machine in the current
	configuration. This file is located in the root of the project:

	touchdesigner_config_and_startup/id.json

	While we've used a number of various techniques 
	for ensuring propper start up, we've found that relying on
	hostname or ip address can produce inconsistent results. 
	For the most reliable configuration it's advisable to avoid the hassle
	this can create and instead use a spearate file to hold
	the role / id information for a given machine.


	'''
	def __init__( self ):

		# put system config file into storage
		self.Load_store_json( 'data/system.json', 'system' )
		self.Load_store_json( 'id.json', 'id' )
		self.System			= project.fetch( 'system' )
		self.Id 			= project.fetch( 'id' )
		self.Store_roles()

		return

	def Load_store_json( self, target_file, storage_key ):
		'''
		
		Arguments
		----------
		target_file ( str ) - 
		storage_key ( str ) - 

		Notes
		---------
		'''

		contents 		= self.Load( target_file )
		json_contents	= json.loads( contents )

		# put contents into storage
		project.store( storage_key, json_contents )

		return

	def Load( self, target_file ):
		'''
		
		Arguments
		----------
		target_file ( str ) -  

		Notes
		---------
		'''

		contents = None

		if os.path.isfile( target_file ):
			
			# format a path and read the file
			target		= open( target_file.format( target_file ), 'r' )
			contents 	= target.read()

			# close file
			target.close()

		else:
		 	error_msg	= missing_file.format( file_name = target_file )
		 	print( error_msg )

		return contents

	def Load_local_config ( self ):
		'''
		
		Arguments
		----------
		NA

		Notes
		---------
		'''	

		# clear storage
		project.unstore( 'local_config' )

		# check for key match:
		system_machine 						= self.Id[ 'id' ] in self.System

		# create a new empty dictionary
		local_config 						= {}

		# create system assignment based on ip
		if system_machine:	
			# print( 'I have a job for you' )
			local_config[ 'host_name' ]		= socket.gethostname()
			local_config[ 'ip_address' ]	= socket.gethostbyname( socket.gethostname() )
			local_config[ 'primary' ]		= self.Id[ 'primary' ]
			local_config[ 'role' ]			= self.System[ self.Id[ 'id' ] ][ 'role' ]
			local_config[ 'tox' ]			= self.System[ self.Id[ 'id' ] ][ 'tox' ]
			local_config[ 'media_path' ]	= self.System[ self.Id[ 'id' ] ][ 'media_path' ]
			local_config[ 'group' ]			= self.System[ self.Id[ 'id' ] ][ 'group' ]
			local_config[ 'outputs' ]		= sum([local_config['group'][projector] for projector in [groupname for groupname in local_config['group']]], [])
			
			project.store( 'local_config' , local_config )

			guest							= False
		
		else:
			guest							= True

		op( 'container_output' ).Touch_init( guest )

		return guest

	def Store_roles( self ):
		'''
		
		Arguments
		----------
		NA

		Notes
		---------
		'''
		roles = []

		system 			= self.System
		sorted_keys 	= sorted( system )

		for item in sorted_keys:
			roles.append( ( item, system[ item ][ 'tox' ] ) )
		
		project.store( "roles", roles )

		return