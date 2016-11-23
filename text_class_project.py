import socket
import json

target_file	= project.folder + '/{file}'
project		= op.Project1

class Config:
	
	def __init__( self ):

		# put system config file into storage
		self.Load_store_json( 'data/system.json', 'system' )
		self.System_id		= self.Load( 'id.txt' )
		self.System			= project.fetch( 'system' )
		self.Store_roles()

		return

	def Load_store_json( self, target_file, storage_key ):

		contents 		= self.Load( target_file )
		json_contents	= json.loads( contents )

		# put contents into storage
		project.store( storage_key, json_contents )

		return

	def Load( self, target_file ):

		# format a path and read the file
		target		= open( target_file.format( target_file ), 'r' )
		contents 	= target.read()

		# close file
		target.close()

		return contents

	def Load_local_config ( self ):
			
			# clear storage
			project.unstore( 'local_config' )

			# check for key match:
			system_machine = self.System_id in self.System

			# create a new empty dictionary
			local_config = {}

			# create system assignment based on ip
			if system_machine:	
				# print( 'I have a job for you' )
				local_config[ 'uri' ]			= self.System_id
				local_config[ 'local_id' ]		= self.System[ self.System_id ][ 'local_ID' ]
				local_config[ 'role' ]			= self.System[ self.System_id ][ 'role' ]
				local_config[ 'tox' ]			= self.System[ self.System_id ][ 'tox' ]
				local_config[ 'media_path' ]	= self.System[ self.System_id ][ 'media_path' ]
				local_config[ 'group' ]			= self.System[ self.System_id ][ 'group' ]
				local_config[ 'outputs' ]		= sum([local_config['group'][projector] for projector in [groupname for groupname in local_config['group']]], [])
				
				project.store( 'local_config' , local_config )

				guest							= False
			
			else:
				guest							= True

			op( 'container_output' ).Touch_init( guest )

			return guest

	def Store_roles( self ):

		roles = []

		system 		= self.System
		sorted_keys = sorted( system )
		
		primary_roles	= [ item for item in sorted_keys if 'primary' in item ]
		backup_roles	= [ item for item in sorted_keys if 'backup' in item ]	

		for role in primary_roles:
			role_pair = ( role, system[ role ][ 'tox' ] )
			roles.append( role_pair )

		for role in backup_roles:
			role_pair = ( role, system[ role ][ 'tox' ] )
			roles.append( role_pair )
		
		project.store( "roles", roles )

		return