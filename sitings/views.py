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
    number_cleaner = re.compile("/^(\d+-?)+\d+$/")
    chem_raw = []
    chems = []
    for chem in cleaned_data:
        if '|' in chem:
            # if not number_cleaner.match(chem):
            chem_raw.append(chem.replace('</td>', '').replace('</n>', '').replace('<n>','').strip().split('|')[-1].encode('ascii','replace').decode('utf-8', 'ignore'))
    for value in chem_raw:
        if not re.match("^\+?(\d+-?)*\d+$", value):
            chems.append(value)
    return render(request, 'sitings/post_detail.html', {'post': post, 'chems':chems})
            # except:
            #     pass``
    # return render(request, 'sitings/post_detail.html', {'post': post, 'x': x})