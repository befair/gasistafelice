from django.db.models.signals import post_syncdb

from gasistafelice.gas.workflow_data import workflow_dict
import workflows 

def init_workflows(sender, app, created_models, verbosity, **kwargs): 
    # `workflows` app was syncronized for the first time
    if workflows.models.Workflow in created_models:
        # now that all necessary tables are in the DB, we can register our workflows
        for name, w in workflow_dict.items():
            w.register_workflow()
            if verbosity == 2:
                # give some feedback to the user
                print "Workflow %s was successfully registered." % name
        return

post_syncdb.connect(init_workflows, sender=workflows.models)
