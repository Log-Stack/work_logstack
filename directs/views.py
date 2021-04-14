from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader, RequestContext
from django.template.loader import get_template
from django.views.generic import ListView

from authy.models import Team, Profile
from directs.models import Message



class DirectsListReceived(ListView):
    template_name = 'directs_list_received.html'
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        if request.POST['action'] == 'Delete':
            print('delete')
            q = request.POST.getlist('delete')
            for pk in q:
                message = get_object_or_404(Message, pk=pk)
                message.is_delete = True
                message.save()
                # message.delete()

            return redirect('directlist_received')

        elif request.POST['action'] == 'Read':
            q = request.POST.getlist('delete')
            for pk in q:
                message = get_object_or_404(Message, pk=pk)
                sender = message.sender
                body = message.body
                title = message.title
                recipient = message.recipient
                message.is_read = True
                message.save()
                message_sender = Message.objects.get(user=sender, sender=sender, title=title, body=body,
                                                     recipient=recipient)
                message_sender.is_read = True
                message_sender.save()
            return redirect('directlist_received')

        elif request.POST['action'] == 'Click':
            if request.POST['check'] == 'true':
                template = get_template('message_list.html')
                message_list = Message.objects.all().filter(user=self.request.user, recipient=self.request.user,
                                             is_delete=False, is_read=False).order_by('-date')
                data = template.render({"message_list": message_list})
            else:
                print('no')
                template = get_template('message_list.html')
                message_list = Message.objects.all().filter(user=self.request.user, recipient=self.request.user,
                                                            is_delete=False).order_by('-date')
                data = template.render({"message_list": message_list})
            return HttpResponse(data)

    def get_queryset(self):
        return Message.objects.all().filter(user=self.request.user, recipient=self.request.user,
                                            is_delete=False).order_by('-date')




class DirectsListSent(ListView):
    # model = Message
    template_name = 'directs_list_sent.html'
    paginate_by = 10


    def post(self, request, *args, **kwargs):
        if request.POST:
            q = request.POST.getlist('delete')
            for pk in q:
                message = get_object_or_404(Message, pk=pk)
                message.is_delete = True

                message.delete()

            return redirect('directlist_sent')

    def get_queryset(self):

        return Message.objects.all().filter(user=self.request.user, sender=self.request.user, is_delete=False).order_by(
            '-date')




class DirectsListDeleted(ListView):
    # model = Message
    template_name = 'directs_list_deleted.html'
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        if request.POST:
            q = request.POST.getlist('delete')
            for pk in q:
                message = get_object_or_404(Message, pk=pk)
                message.delete()

            return redirect('directs_deleted')

    def get_queryset(self):
        return Message.objects.all().filter(user=self.request.user, recipient=self.request.user,
                                            is_delete=True).order_by('-date')


@login_required
def directs_send(request):
    if request.method == "POST":
        from_user_id = request.user.id
        from_user = User.objects.get(id=from_user_id)
        title = request.POST.get('title')
        body = request.POST.get('body')
        user_id = request.POST.get('user')

        to_user = User.objects.get(id=user_id)

        Message.send_message(from_user, to_user, title, body)

        # return redirect('directlist_sent')
        return HttpResponse('ok')
    else:
        HttpResponseBadRequest()

    template = loader.get_template('directs_send.html')

    return HttpResponse(template.render({}, request))


@login_required
def directs_reply(request, pk):
    message_id = pk
    receiver = Message.objects.get(pk=pk).sender

    if request.method == "POST":
        from_user_id = request.user.id
        from_user = User.objects.get(id=from_user_id)
        title = request.POST.get('title')
        body = request.POST.get('body')
        to_user = User.objects.get(username=receiver)

        Message.send_message(from_user, to_user, title, body)

        return redirect('directlist_sent')
    else:
        HttpResponseBadRequest()

    context = {
        'receiver': receiver
    }
    template = loader.get_template('directs_reply.html')
    return HttpResponse(template.render(context, request))


@login_required
def directs_detail(request, pk, lst):
    message = Message.objects.get(pk=pk)
    sender = message.sender
    body = message.body
    title = message.title
    recipient = message.recipient
    if lst==1:
        if not message.is_read:
            message.is_read = True
            message.save()
            message_sender = Message.objects.get(user=sender, sender=sender,title=title,body=body,recipient=recipient)
            message_sender.is_read=True
            message_sender.save()


    print(message.is_read_date)

    template = loader.get_template('directs_detail.html')
    if request.method == "POST":
        print(request.user)
    else:
        HttpResponseBadRequest()

    context = {
        'message': message
    }
    return HttpResponse(template.render(context, request))


@login_required
def directs_detail_delete(request, pk, lst):
    if lst == 1:
        message = Message.objects.get(pk=pk)
        user = message.user
        message = Message.objects.get(pk=pk, user=user, recipient=user)
        message.is_delete = True
        message.save()
        return redirect('directlist_received')
    elif lst == 2:
        message = Message.objects.get(pk=pk)
        user = message.user
        message = Message.objects.get(pk=pk, user=user, sender=user)
        message.is_delete = True
        message.save()
        return redirect('directlist_sent')
    else:
        message = Message.objects.get(pk=pk)
        user = message.user
        message = Message.objects.get(pk=pk, user=user, recipient=user)
        message.delete()
        return redirect('directs_deleted')


def checkDirects(request):
    directs_count = 0
    if request.user.is_authenticated:
        directs_count = Message.objects.all().filter(user=request.user, recipient=request.user, is_read=False).count()

    return {'directs_count': directs_count}
