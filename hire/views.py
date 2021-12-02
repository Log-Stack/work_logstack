from django.http import FileResponse, Http404
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .forms import PersonForm, Person
from .models import Hit


def inputPage(request):
    if request.method == "POST":
        form = PersonForm(request.POST, request.FILES)
        if Person.objects.filter(name=request.POST['name'], phone=request.POST['phone']).exists():
            error = '귀하는 이미 지원하셨습니다.\n과제 안내를 위해 곧 연락 드릴게요 :)'
            return render(request, 'apply_input.html', {'form': form, 'error': error})
        elif '@' not in request.POST['email'] or '.' not in request.POST['email'] or len(request.POST['phone']) < 11:
            error = '지원에 실패하셨습니다.\n입력한 내용을 다시 한번 확인 부탁드립니다.'
            return render(request, 'apply_input.html', {'form': form, 'error': error})
        # elif request.FILES.get('file', False) and '.pdf' not in request.FILES['file'].name:
        #     error = '파일 양식이 올바르지 않습니다.\n입력한 내용을 다시 한번 확인 부탁드립니다.'
        #     return render(request, 'apply_input.html', {'form': form, 'error': error})
        elif form.is_valid():
            form.save()
            import requests
            requests.get('https://www.first-class.co.kr/push/push/test/')
            error = '지원해주셔서 감사드립니다.\n곧 연락드릴게요. :)'
            return render(request, 'apply_input.html', {'error': error})
        else:
            # error = '지원에 실패하셨습니다.\n입력한 내용을 다시 한번 확인 부탁드립니다.'
            error = form.errors
            return render(request, 'apply_input.html', {'form': form, 'error': error})
    else:
        form = PersonForm()
        response = render(request, 'apply_input.html', {'form': form})

        expire_date, now = timezone.now(), timezone.now()
        expire_date += timezone.timedelta(days=1)
        expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
        max_age = (expire_date - now).seconds

        cookie_value = request.COOKIES.get('hitboard', '_')

        if 'apply' not in cookie_value:
            cookie_value += 'apply_'
            response.set_cookie('hitboard', value=cookie_value, max_age=max_age, httponly=True)
            hit, _ = Hit.objects.get_or_create(date=timezone.now().date())
            hit.count += 1
            hit.save()

        return response


def applyList(request):
    if request.method == "GET":
        return render(request, 'apply_list.html', {'result': Person.objects.all(), 'hit': Hit.objects.get_or_create(date=timezone.now())[0].count, 'date':timezone.now().date()})


def applyDetail(request, pk):
    if request.method == "GET":
        return render(request, 'apply_detail.html', {'profile': Person.objects.get(pk=pk)})


def pdf(request, name):
    try:
        return FileResponse(open(f'/home/ubuntu/workLog/media/{name}', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404('not found')