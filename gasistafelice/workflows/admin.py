from django.contrib import admin
from gasistafelice.workflows.models import State
from gasistafelice.workflows.models import StateInheritanceBlock
from gasistafelice.workflows.models import StatePermissionRelation
from gasistafelice.workflows.models import StateObjectRelation
from gasistafelice.workflows.models import Transition
from gasistafelice.workflows.models import Workflow
from gasistafelice.workflows.models import WorkflowObjectRelation
from gasistafelice.workflows.models import WorkflowModelRelation
from gasistafelice.workflows.models import WorkflowPermissionRelation

class StateInline(admin.TabularInline):
    model = State

class WorkflowAdmin(admin.ModelAdmin):
    inlines = [
        StateInline,
    ]

admin.site.register(Workflow, WorkflowAdmin)

admin.site.register(State)
admin.site.register(StateInheritanceBlock)
admin.site.register(StateObjectRelation)
admin.site.register(StatePermissionRelation)
admin.site.register(Transition)
admin.site.register(WorkflowObjectRelation)
admin.site.register(WorkflowModelRelation)
admin.site.register(WorkflowPermissionRelation)
