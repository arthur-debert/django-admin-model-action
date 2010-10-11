from django.contrib import admin
from django.contrib import messages

class ModelAction(object):
    def __init__(self, action_method, action_name, can_act_method=None):
        self.action_method = action_method
        self.action_name = action_name
        self.can_act_method = can_act_method

    @property    
    def name(self):
        return self.action_name

    @property
    def form_name(self):
        return self.name.lower().replace(" ", "-")
    
    def can_act_for(self, request, obj):
        if self.can_act_method is not None:
            if isinstance(self.can_act_method, str):
                return getattr(obj, self.can_act_method)(request)
            else:
                return self.can_act_method(request, obj)
        else:
            return True

    def do_action(self, request, obj):
        if isinstance(self.action_method, str):
            msg =  getattr(obj, self.action_method)(request)
        else:
            msg =  self.action_method(request, obj)
        if msg is None:
            msg = "%s is done." % self.action_name
        messages.success(request, msg)    
            
    def __unicode__(self):
        return "ModelAction %s" % self.action_name
    
class ActionAdmin(admin.ModelAdmin):
    model_actions = []

    change_form_template = "adminmodelaction/model-action-change-form.html"
    
    def __init__(self, model, admin_site):
        super(ActionAdmin, self).__init__(model, admin_site)
        self.model_actions = [ModelAction(*action_options) for action_options in self.model_actions]

    def get_model_actions_for(self, request, obj):
        return [action for action in self.model_actions if action.can_act_for(request, obj)]

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
            response = self.response_change(request, obj)        
        else:
            response =  super(ActionAdmin, self).change_view(request, object_id, extra_context)
        return response
