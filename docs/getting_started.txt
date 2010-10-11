Getting Started
===============

To get started using ``django-admin-model-action`` simply install it with
``pip``::

    $ pip install django-admin-model-action

Quick start::
- Add adminmodelaction to your ``INSTALLED_APPS``.
- On your model admin, inherit from ```ActionAdmin```.
- Specify the action method to run (as a string pointing to a model's method, or a regular method). Example::

    from adminmodelaction.admin import ActionAdmin

    class EntryAdmin(ActionAdmin):
        model_actions = ['publish']
        model = Entry

And then on your Article model::

    class Article(models.Model):
        #... definitions go here ...
        
        def can_publish_article(self, request):
            # this is optional: it's a hook that allows you not to display
            # this action for a given model.
            # in this example, we only allow publishing of non public articles
            # in order not to notify author twice
            return !self.public
            
        def publish(self, request):
            self.public=True
            notify_author(self.author, self.title)
            # the admin message will be return result from this method
            return "Your entry %s was published." % (self.title).
        publish.short_description = 'Publish Article'    
        publish.can_add_action = can_publish_article
            
This will create a "Publish Article" button on top of each article's change view on the admin.
Once an admin clicks on it, the 'publish' method will be called on the Article's instance. In this case, for example
publishing an article will change it's ```public``` property, and also notify the author.

By using the optional ```action_method.can_add_action``` we make sure the action will only appear to models not published already.