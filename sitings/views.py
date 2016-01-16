from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
import requests
from bs4 import BeautifulSoup
import re

def post_list(request):
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
    post = get_object_or_404(Post,pk=pk)
    url = 'http://pkuxxj.pku.edu.cn/UNPD/print_fz_zwln.php'
    r = requests.post(url, data={'fangji':str(post)})
    plant_data = r.content
    BS_data = BeautifulSoup(plant_data, "lxml")
    decoded_data = BS_data.decode('utf-8')
    cleaned_data = decoded_data.split('<td>\n')
    number_cleaner = "^\+?(\d+-?)*\d+$"
    chem_raw = []
    chems = []
    flavanoids = ('one','in',)
    flavanoid_count = 0
    terpenes = ('sterol', 'ene', 'ol','en','enin',)
    terpene_count = 0
    amines = ('ine',)
    amine_count = 0
    acids = ('acid','saeure',)
    acid_count = 0
    glycoside_count = 0

    for chem in cleaned_data:
        if '|' in chem:
            chem_raw.append(chem.replace('</td>', '').replace('</n>', '').replace('<n>','').strip().split('|')[-1].
            encode('ascii','replace').decode('utf-8', 'ignore'))
    for value in chem_raw:
        if not re.match(number_cleaner, value):
            chems.append(value)
    for compound in chems:
        if compound.endswith(flavanoids):
            flavanoid_count += 1
        elif compound.endswith(terpenes):
            terpene_count += 1
        elif compound.endswith(amines):
            amine_count += 1
        elif compound[:-2].endswith('side') or compound.endswith('side'):
            glycoside_count += 1

    return render(request, 'sitings/post_detail.html', {'post': post, 'chems':chems, 
    'flavanoid_count':flavanoid_count, 'terpene_count':terpene_count, 'amine_count':amine_count, 'acid_count':acid_count,
    'glycoside_count':glycoside_count})