from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader


@login_required
def directs_list(request):

    template = loader.get_template('directs_list.html')
    context = {

    }
    return HttpResponse(template.render(context,request))


# @login_required
# def SendDirect(request):
#     from_user = request.user
#     to_user_username = request.POST.get('to_user')
#     body = request.POST.get('body')
#
#     if request.method == 'POST':
#         to_user = User.objects.get(username=to_user_username)
#         Message.send_message(from_user, to_user, body)
#         return redirect('inbox')
#     else:
#         HttpResponseBadRequest()
#
#
@login_required
def directs_send(request):



    template = loader.get_template('directs_send.html')
    context = {

    }
    return HttpResponse(template.render(context,request))


@login_required
def directs_read(request):

    template = loader.get_template('directs_read.html')
    context = {

    }
    return HttpResponse(template.render(context,request))