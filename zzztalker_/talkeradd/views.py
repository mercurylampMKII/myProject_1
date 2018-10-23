from django.shortcuts import render
from .models import Counters, Foodnews
# Create your views here.
def index(request):
    return render(request, "talkeradd/bg-manage-add.html");

def add(request):
    if request.method =='POST':
        obj =Counters.objects.all()[0]
        update_seq = obj.seq_value + 1
        coun =Counters.addCounters('talkid', update_seq)
        coun.save()
        id = update_seq
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        images = request.POST.get('images')
        tfoodnews = Foodnews.addFoodnews(id, title, content, category, images)
        tfoodnews.save()
    return render(request, 'talkeradd/bg-manage-add.html');