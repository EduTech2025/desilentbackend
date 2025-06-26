from django.http import HttpResponse

def home(request):
    return HttpResponse("✅ Django is up and running!")
