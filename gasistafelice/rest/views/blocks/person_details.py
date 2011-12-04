"""View for block details specialized for a Person"""

from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

from gasistafelice.rest.views.blocks import details


class Block(details.Block):

    BLOCK_NAME = "person_details"
    BLOCK_VALID_RESOURCE_TYPES = ["gasmember", "person"] 

    def _get_user_actions(self, request):

        return []

    def get_description(self):
        return _("Who is %(name)s?") % {
            'name' : self.resource.person.name,
        }

    @property
    def resource(self):
        return self._resource.person

    @resource.setter
    def resource(self, value):
        self._resource = value

