
import pickle
import base64

from django.utils.translation import ugettext_lazy as _, string_concat, ugettext
from django.db import models
from django.db.models import Model, permalink
from django.contrib.auth.models import User

#-----------------------------------------------------------------------------#
# CONSTANTS                                                                   #
#-----------------------------------------------------------------------------#
PICKLE_USED_PROTOCOL = 2
REST_TABLE_SPACE = 'restts'

#-----------------------------------------------------------------------------#
# TABLES                                                                      #
#-----------------------------------------------------------------------------#

class BlockConfiguration(Model):
	
	user          = models.ForeignKey(User, db_index=True, verbose_name=_('User'))
	
	blocktype     = models.CharField(max_length=255, blank=True, db_index=True, verbose_name=_('Rest block name'))	
	
	resource_type = models.CharField(max_length=255, null=False, blank=False, db_index=True, verbose_name=_('Resource type'))	
	resource_id   = models.CharField(max_length=255, null=False, blank=False, db_index=True, verbose_name=_('Resource key'))	

	page          = models.SmallIntegerField(default=1, null=False, blank=False, verbose_name=_('user page'), db_index=False)
	position      = models.SmallIntegerField(default=0, null=False, blank=False, verbose_name=_('page position'), db_index=False)
	
	confdata      = models.TextField(default='', null=True, db_index=False, verbose_name=_('Configuration data'))
	
	#-----------------------------------------------------------------------------#
	
	def __unicode__(self):
		return "[%s]%s/%s/%s/%s/%s" % (self.user.username, self.page, self.resource_type, self.resource_id, self.blocktype, self.get_configuration())
	
	
	#-----------------------------------------------------------------------------#
	
	def get_configuration(self):
		
		conf = {}
		try:
			binary_data = base64.b64decode(self.confdata)		
			conf        = pickle.loads(binary_data)		
		except pickle.PickleError, e:
			pass
		except Exception, e:
			pass

		return conf		
	
	def set_configuration(self, options_dict):
		
		# Serializing and saving
		try:
			binary_data   = pickle.dumps(options_dict, PICKLE_USED_PROTOCOL)
			self.confdata = base64.b64encode(binary_data)		
		except pickle.PickleError, e:
			raise Exception("Impossibile serializzare la configurazione : %s", str(e))
		except Exception, e:
			raise Exception("Impossibile serializzare la configurazione : %s", str(e))

	#-----------------------------------------------------------------------------#
	
	class Meta:
		verbose_name = "Block configuration data"
		db_table = "blockconfiguration"
		
		db_tablespace = REST_TABLE_SPACE
		
def remove_displayed_blocks_from_userpage_by_user(user, printout=None):
	
	from users.models import can_access_to_resource
	from state.models import type_model_d
	key_column = {
		'site'         :'name',
		'iface'        :'name',
		'target'       :'expanded_title',
		'measure'      :'path',
		'node'         :'name',
		'container'    :'name',
		'usercontainer':'name',
	}	
	
	
	for b in BlockConfiguration.objects.filter(user=user):
		
		resource_class = type_model_d[ b.resource_type ]
		r = resource_class.objects.get(id=int(b.resource_id))
		
		if not can_access_to_resource(user, r):
			if printout:
				printout("removing block %s from %s's userpage" % (b, user))
			b.delete()
			
def remove_displayed_blocks_from_userpage_by_resource(resource, printout=None):
	
	from users.models import can_access_to_resource
	
	resource_type = resource.__class__.__name__.lower()
	resource_id   = resource.id

	for b in BlockConfiguration.objects.filter(resource_type=resource_type, resource_id=str(resource_id) ):
		
		user = b.user
		
		if not can_access_to_resource(user, resource):
			if printout:
				printout("removing block %s from %s's userpage" % (b, user))
			b.delete()
