from django.core.checks import messages
from django.db import IntegrityError
from django.contrib import messages
from django.db import models
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse
from django.views import generic
from django.views.generic.base import RedirectView
# Create your views here.
from .models import Group,GroupMember
class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields =  ('name','description')
    model =Group

class SingleGroup(generic.DetailView):
    model = Group
class ListGroup(generic.ListView):
    model = Group
class JoinGroup(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user,group=group )
        except IntegrityError:
            messages.warning(self.request,('warning already amember'))
        else:
            messages.success(self.request,'You are now a member')
        return super().get(request,*args,**kwargs)

class LeaveGroup(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
    def get(self, request, *args, **kwargs):
        try:
            membership = GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request,"sorry you r not i  this group")
        else:
            membership.delete()
            messages.success(self.request,'You have left the group')
        return super().get(request, *args, **kwargs)