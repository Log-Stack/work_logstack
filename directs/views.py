from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template import loader
from django.views.generic import ListView

from authy.models import Team, Profile
from directs.models import Message


@login_required
def directs_list_received(request):

    template = loader.get_template('directs_list_received.html')
    context = {

    }
    return HttpResponse(template.render(context,request))


# @login_required
# def directs_list_sent(request):
#     from_user = request.user
#
#     messages_sent = Message.objects.all().filter(sender=from_user)
#     p = Paginator(messages_sent,10)
#     print(p.num_pages)
#     template = loader.get_template('directs_list_sent.html')
#     context = {
#         'messages':messages_sent,
#         'pages':[p.num_pages],
#     }
#     return HttpResponse(template.render(context,request))


class DirectsListSent(ListView):

    model = Message
    template_name = 'directs_list_sent.html'
    ordering = '-date'
    paginate_by = 10




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
def directs_read(request,pk):
    print(pk)
    template = loader.get_template('directs_detail.html')
    context = {

    }
    return HttpResponse(template.render(context,request))