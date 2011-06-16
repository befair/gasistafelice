import re

from djlabs.shortcuts import render_to_response

from django.contrib.auth.models import User

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class AbstractBlock(object):
	
	#------------------------------------------------------------------------------#
	#                                                                              #
	#------------------------------------------------------------------------------#
	
	def __init__(self):
		
		self.app          = 'rest'
		
		self.loc          = 'body'

		self.name         = ''
		self.description  = ''
		
		self.auto_refresh = False
		self.refresh_rate = 0

		self.start_open   = False
	
	#------------------------------------------------------------------------------#
	#                                                                              #
	#------------------------------------------------------------------------------#

	@property
	def block_name(self):
		return self.name
		
	#------------------------------------------------------------------------------#
	#                                                                              #
	#------------------------------------------------------------------------------#		
	
	def is_valid(self, resource_type):
		"""
		Returns true if the block is valid for the given resource_type
		"""
		return True
		
	#------------------------------------------------------------------------------#
	#                                                                              #
	#------------------------------------------------------------------------------#		
	
	def visible_in_page(self):
		"""
		Return true if the block can be added in user page.
		"""
		return True

	#------------------------------------------------------------------------------#
	#                                                                              #
	#------------------------------------------------------------------------------#		
	
	def get_description(self):
		return self.description

	#------------------------------------------------------------------------------#
	#                                                                              #
	#------------------------------------------------------------------------------#		
	
	def options_response(self, request, resource_type, resource_id):
		#
		# No options by default
		#
		ctx={
			#'block_name' : 'Details',
			'fields': []
		}
		return render_to_response('options.xml', ctx)

	def validate_options(self, options_dict):
		# return no errors for user options
		return None

	#------------------------------------------------------------------------------#
	#                                                                              #
	#------------------------------------------------------------------------------#		
	
	def get_response(self, request, resource_type, resource_id, args):
		return ""

	#------------------------------------------------------------------------------#
	#                                                                              #
	#------------------------------------------------------------------------------#
	
	def create_block_signature(self, resource_type, resource_id):
		
		from state.models import type_model_d
		
		resource_class = type_model_d[resource_type]
		
		resource = resource_class.objects.get(id=int(resource_id))
		
		return self.create_block_signature_from_resource(resource)
		
	def create_block_signature_from_resource(self, resource):
		
		block_urn = '%s/%s/%s/' % (resource.resource_type, resource.id, self.name)
		
		return '<block \
		             block_name="%s" \
		             block_description="%s" \
		             \
		             block_urn="%s" \
		             resource_name="%s" \
		             \
		             refresh_rate="%s" \
		             auto_refresh="%s" \
		             start_open="%s" \
		        />' % (
			self.block_name,
			'%s' % (str(self.get_description())),
			block_urn,
			str(resource),
			self.refresh_rate,
			str(self.auto_refresh).lower(),
			str(self.start_open).lower(),
		)

	#------------------------------------------------------------------------------#		
	# Useful methods                                                               #
	#------------------------------------------------------------------------------#		

	def load_user_configuration(self, user, resource_type, resource_id):
	
		from rest.models import BlockConfiguration
		
		config = None
		
		try:
			blocks_conf = BlockConfiguration.objects.get(blocktype=self.block_name
								       ,user=user
								       ,resource_type=resource_type
								       ,resource_id=resource_id
								       )
								       
			config = blocks_conf.get_configuration()
			
			config = self.from_xml_to_dict(config)
			
			return config			
			
		except Exception, e:
			pass

		return config 
	
	def from_xml_to_dict(self, xml_string):
		from xml.dom import minidom
		
		d = {}
		xmldoc = minidom.parseString(xml_string)             
		
		for param in xmldoc.getElementsByTagName("param"):
			name = param.attributes['name'].value
			val  = param.attributes['value'].value
			
			d[name] = val

		return d



	def read_cookie(self, resource_type, resource_id, cookie):
		
		d = {}
		for k,v in cookie.items():
			
			# block_<app>_<resource type>_<resource_id>_<block_name>_ + _<var_name> = <val>
			
			parts = k.split('__')
			if len(parts) != 2: continue
			
			block_id = parts[0]
			var_name = parts[1]
			
			if block_id[ -len(self.name) : ] != self.name: continue
			block_id = block_id[ : - (1+len(self.name)) ] 

			(dummy, app, t, i) = re.split('_', block_id)
			
			if app != self.app:
				continue
				
			if t == resource_type and i == resource_id:
				
				d[var_name] = v
				
		return d
