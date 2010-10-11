from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect


ACTION_DESCRIPTION_NAME = 'short_description'
ACTION_CAN_CALL_FUNC_NAME = 'can_add_action'

class ModelAction(object):
    form_prefix = "__model_action-"
    def __init__(self, action_method,  model):
        if not callable(action_method):
            action_method = getattr(model, action_method)
        self.action_method = action_method
        self.action_name = getattr(self.action_method, ACTION_DESCRIPTION_NAME,  u"Model Action (please set a 'short_description' attribute on your method '%s')" % (self.action_method.__name__))
        self.can_add_action = getattr(self.action_method, ACTION_CAN_CALL_FUNC_NAME, None)

    @property    
    def name(self):
        return self.action_name

    @property
    def form_name(self):
        return u"%s%s" % (self.form_prefix, self.name.lower().replace(" ", "-"))

    def can_act_for(self, request, obj):
        if self.can_add_action:
            return self.can_add_action( request, obj)
        return True

    def do_action(self, request, obj):
        msg =  self.action_method( obj, request)
        if msg is None:
            msg = "%s is done." % self.action_name
        messages.success(request, msg)    
            
    def __unicode__(self):
        return u"ModelAction %s" % self.action_name.__name__
    
class ActionAdmin(admin.ModelAdmin):
    model_actions = []

    change_form_template = "adminmodelaction/model-action-change-form.html"
    
    def __init__(self, model, admin_site):
        super(ActionAdmin, self).__init__(model, admin_site)
        self.model_actions = [ModelAction(*action_options, model=model) for action_options in self.model_actions]

    def get_model_actions_for(self, request, obj):
        return [action for action in self.model_actions if action.can_act_for ( request, obj)]

    def change_view(self, request, object_id, extra_context=None):
        if extra_context is None:
            extra_context = {}
        obj = self.get_object(request, admin.util.unquote(object_id))    
        extra_context['model_actions'] = self.get_model_actions_for(request, obj)
        if request.POST.has_key('is_model_action'):
            for action in self.model_actions:
                form_name = action.form_name
                if request.POST.has_key(form_name):
                    action.do_action(request, obj)
            response = HttpResponseRedirect(request.path)
        else:
            response =  super(ActionAdmin, self).change_view(request, object_id, extra_context)
        return response
