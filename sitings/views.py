from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
import requests
from bs4 import BeautifulSoup
import re
from unidecode import unidecode as un


def post_list(request):
    """
    A function that retrieves and returns plant siting posts information ordered by decreasing published date.  
    For the submission form in the page if a POST request is detected, save the inputted information and return it to the database.
    Otherwise, render an empty form"""
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("/")
    elif request.method == "GET":
        form = PostForm()
    return render(request, 'sitings/post_list.html', {'posts': posts, 'form':form})

def post_detail(request, pk):
    """ After clicking a plant siting on the main page send the plant name to a natural products database, 
    scrape the contents and return chemicals found in the plant/mushroom.  Count the chemicals according 
    to chemical structure by checking suffixes and send the count of compounds to the page to be displayed

    """
    post = get_object_or_404(Post,pk=pk)
    url = 'http://pkuxxj.pku.edu.cn/UNPD/print_fz_zwln.php'
    r = requests.post(url, data={'fangji':str(post)}) #Insert the plant name into the input box
    plant_data = r.content
    BS_data = BeautifulSoup(plant_data, "lxml")
    decoded_data = BS_data.decode('utf-8') #Convert from bytes to string
    cleaned_data = decoded_data.split('<td>\n')
    number_cleaner = "^\+?(\d+-?)*\d+$" #Regex to remove extraneous numbers (e.g. 23-5124-1251)
    chem_raw = []
    chems = []
    flavonoids = ('one','in',)
    flavonoid_count = 0
    terpenes = ('sterol', 'ene', 'ol','en','enin',)
    terpene_count = 0
    amines = ('ine',)
    amine_count = 0
    acids = ('acid','saeure',)
    acid_count = 0
    glycoside_count = 0


    for chem in cleaned_data:
        if '|' in chem:
            chem_raw.append((chem.replace('</td>', '').replace('</n>', '').replace('<n>','').strip().split('|')[-1].
            capitalize())) #identify tr elements containing chemicals by the presence of |
            # The | is used to separate chemical synonyms and only one name is wanted so the last one is retrieved
            # Example: compounds = 'Bicyclo[3.1.1.]hept-2-ene,2,6,6-trimethyl | 2-Pinene' ---> result = '2-Pinene'
            # Stray html tags also have to be removed and the encoding and decoding is to avoid the script breaking when greek unicode
            #characters are in a compound (e.g. β-Sitosterol)
    for value in chem_raw:
        if not re.match(number_cleaner, value): #Remove strings composed of only numbers and dashes
            chems.append(value)  
    for compound in chems: # Check the suffixes and count occurrences
        if compound.endswith(flavonoids):
            flavonoid_count += 1
        elif compound.endswith(terpenes):
            terpene_count += 1
        elif compound.endswith(amines):
            amine_count += 1
        elif compound[:-2].endswith('side') or compound.endswith('side'):
            glycoside_count += 1
        if compound.endswith(acids):
            acid_count += 1

    return render(request, 'sitings/post_detail.html', {'post': post, 'chems':sorted(chems), 
    'flavonoid_count':flavonoid_count, 'terpene_count':terpene_count, 'amine_count':amine_count,
    'acid_count':acid_count, 'glycoside_count':glycoside_count})