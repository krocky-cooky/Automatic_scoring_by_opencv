from django.shortcuts import render
from .models import Test
from .forms import TestForm
from django.views.generic import FormView
from django.http import JsonResponse
from keisanki import settings
from . import detect

# Create your views here.
class TestView(FormView):
    template_name = 'saiten/test.html'
    form_class = TestForm

def ajax_saiten(request):
    if request.method == 'POST':
        res = {}
        posted_file = request.FILES['file']
        new_test = Test.objects.create(file=posted_file)
        input_url =  settings.BASE_DIR + new_test.file.url
        output_url = settings.BASE_DIR + '/media/output.png' 
        student_number,score,table_dict = detect.saiten(input_url,output_url)
    
        res['file_url'] = '/media/output.png'
        res['student_number'] = student_number
        res['score'] = score
        res['table'] = table_dict
        return JsonResponse(res,status=201)

