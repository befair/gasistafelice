 
# Copyright (C) 2011 Rete di Economia Etica e Solidale <http://www.reesmarche.org>
# taken from SANET - Laboratori Guglielmo Marconi S.p.A. <http://www.labs.it>
#
# This file is part of GASISTA FELICE
# GASISTA FELICE is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License
#
# GASISTA FELICE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with GASISTA FELICE. If not, see <http://www.gnu.org/licenses/>.

"""Unique resource name.

This module offer a unique class for managing resource context
"""

#-------------------------------------------------------------------------------

class URN(list):
    #TODO placeholder seldon: translate
	"""Questa classe e' utile per generalizzare la gestione del percorso di un oggetto.
	Una istanza e' rappresentata da una gerarchia che parte dall'oggetto sito

	La classe e' una lista i cui elementi sono il percorso dell'oggetto 
	L'oggetto che rappresenta il contesto e' l'elemento in coda allo stack

	Prende in input
	@param resource_list = lista di risorse istanziate appartenenti all'urn
	"""

	def __init__(self, resource_list):

		super(URN, self).__init__(resource_list)
		self.name_list = [] #convenient name cache
		for el in self:
			self.name_list.append(el.name)
		self.resource = self[-1]

	def __str__(self):
		# Represent the URN path. 
		# Each element is in the form $res_type-$res_id
		rv = ""
		for resource in self:
			rv += "/" + resource.__class__.__name__.lower() + "-" + str(resource.id) 
		return rv

	def __unicode__(self):
		return str(self)

	def __repr__(self):
		return "/".join(self.name_list) + "/"

	def __nonzero__(self):
		# This object evaluates to False only if every value resource is empty
		rv = False
		for v in self:
			if v : rv = True
		return rv 

