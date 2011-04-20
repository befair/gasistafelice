from django.db.models.signals import post_syncdb

from gasistafelice.gas.workflow_data import workflow_dict

def init_workflows(app, created_models, verbosity, **kwargs):
    app_label = app.__name__.split('.')[-2]
    if app_label == 'workflows' and created_models: # `worklows` app was syncronized for the first time
        # now that all necessary tables are in the DB, we can register our workflows
        for (name, w) in workflow_dict:
            w.register_workflow()
            if verbosity == 2:
                # give some feedback to the user
                print "Workflow %s was successfully registered." % name    
        return

post_syncdb.connect(init_workflows)
