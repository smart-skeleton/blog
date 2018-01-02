from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from blog.models import EMG
from django.http import Http404

from blog.forms import ContactForm
from blog.forms import dataForm
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template
from django import db

# Create your views here.

def index(request):
    return render(request, "blog/index.html")

def contact(request):
    form_class = ContactForm
    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
            , '')
            contact_email = request.POST.get(
                'contact_email'
            , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the 
            # contact information
            template = get_template('blog/contact_template.txt')
            context = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            })
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                ['skeleton.smart@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('contact')

    return render(request, 'blog/Contact.html', {
        'form': form_class,
    })  


def pictures(request):
    return render(request, "blog/Pictures.html")

def news(request):
    return render(request, "blog/News.html")

def data(request):
    #db.connections.close_all()
    form_class = dataForm
    if request.method == 'GET':
        form = form_class(data=request.GET)
        if form.is_valid():
            data = request.GET.get('data', '')
            b = EMG(valeur= data)
            form.save()

    try:
    	emg = EMG.objects.all()
    except emg.DoesNotExist:
        raise Http404

    return render(request, 'blog/Data.html', {'data': emg})



def date_actuelle(request):
    return render(request, 'blog/date.html', {'date': datetime.now()})


def addition(request, nombre1, nombre2):    
    total = int(nombre1) + int(nombre2)

    # Retourne nombre1, nombre2 et la somme des deux au tpl
    return render(request, 'blog/addition.html', locals())

def home(request):
    """ Exemple de page HTML, non valide pour que l'exemple soit concis """
    text = """<h1>Bienvenue sur Smart Skeleton</h1>
              <p>Une nouvelle génération de prothése, exosquelette et intélligente</p>"""
    return HttpResponse(text)


def accueil(request):
    """ Afficher tous les articles de notre blog """
    articles = Article.objects.all() # Nous sélectionnons tous nos articles
    return render(request, 'blog/accueil.html')

def lire(request, id):
    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        raise Http404

    return render(request, 'blog/lire.html', {'article': article})








