from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template import loader

from authy.models import Team, Profile
from directs.models import Message


@login_required
def directs_list_received(request):

    template = loader.get_template('directs_list_received.html')
    context = {

    }
    return HttpResponse(template.render(context,request))


@login_required
def directs_list_sent(request):
    user = request.user

    template = loader.get_template('directs_list_sent.html')
    context = {

    }
    return HttpResponse(template.render(context,request))




@login_required
def directs_send(request):
    if request.method == "POST":
        from_user = request.user
        title = request.POST.get('title')
        body = request.POST.get('body')
        user_id = request.POST.get('user')
        to_user = User.objects.get(id=user_id)

        Message.send_message(from_user,to_user,title,body)

        return redirect('directlist_received')
    else:
        HttpResponseBadRequest()

    template = loader.get_template('directs_send.html')

    return HttpResponse(template.render({},request))



@login_required
def directs_read(request):

    template = loader.get_template('directs_read.html')
    context = {

    }
    return HttpResponse(template.render(context,request))