from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader


@login_required
def directs_list(request):

    template = loader.get_template('directs_list.html')
    context = {

    }
    return HttpResponse(template.render(context,request))

@login_required
def directs_send(request):

    template = loader.get_template('directs_send.html')
    context = {

    }
    return HttpResponse(template.render(context,request))
