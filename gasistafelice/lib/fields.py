 
# Copyright (C) 2008 Laboratori Guglielmo Marconi S.p.A. <http://www.labs.it>
#
# This file is part of SANET
# SANET is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License
#
# SANET is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with SANET. If not, see <http://www.gnu.org/licenses/>.


from django.db import models

class Resource(models.CharField):
    """A fake field class to correctly display resource vertically"""
    pass

class ResourceList(models.CharField):
    """A fake field class to correctly display resource list vertically"""
    pass

class ResourceListInline(models.CharField):
    """A fake field class to correctly display resource list horizontally"""
    pass

class HTMLField(models.TextField):
    """A fake field class to include HTML content"""
    pass
