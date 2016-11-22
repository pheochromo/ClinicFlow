from django.shortcuts import render

def manage(request):
    return render(request, 'manage.html')
    
def viewer(request):
    return render(request, 'viewer.html')    
    
def login(request):
    return render(request, 'login.html')      
