from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mayphat.models import Category, Baotri, Imageslide
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    moi = Category.objects.all().filter(status='New')
    noibat = Category.objects.all().filter(status='Old')
    return render(request, "trangchu.html", {'moi': moi, 'noibat': noibat})


def maycu(request):
    category = Category.objects.all().filter(status='Old')
    paginator = Paginator(category, 6)
    pageNumber = request.GET.get('page')
    try:
        customers = paginator.page(pageNumber)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)

    return render(request, "mayphatcu.html", {'category': customers, 'page': range(1, paginator.num_pages + 1)})


def maychothue(request):
    if 'cart' in request.session:
        del request.session['cart']
    category = Category.objects.all()
    paginator = Paginator(category, 6)
    pageNumber = request.GET.get('page')
    try:
        customers = paginator.page(pageNumber)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)

    return render(request, "maychothue.html", {'category': customers, 'page': range(1, paginator.num_pages + 1)})


def maymoi(request):
    if 'cart' not in request.session:
        request.session['cart'] = []
    cart = request.session['cart']
    # dont expire untill the browser is closed
    request.session.set_expiry(0)

    category = Category.objects.all().filter(status='New')
    paginator = Paginator(category, 6)
    pageNumber = request.GET.get('page')
    try:
        customers = paginator.page(pageNumber)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)
    if request.method == "POST":
        # will add the object that they have posted to the card.
        # we called our form object input object ID . the input name = "obj_id"
        # after clicking to addToItem  => the item will add to cart by its porduct.id as value and obj_id as name in input
        cart.append(int(request.POST['obj_id']))
        # catalog is the name of the main page
        return redirect('maymoi')
    return render(request, "maymoi.html",
                  {'category': customers, 'page': range(1, paginator.num_pages + 1), 'cart_size': len(cart)})


def baotri(request):
    vkey = request.GET.get('thongtin')
    baotrimay = Baotri.objects.all().filter(title_name=vkey)
    return render(request, "baotri.html", {'baotrimay': baotrimay})


def giohang(request):
    if 'cart' not in request.session:
        request.session['cart'] = []
    cart = (request.session['cart'])
    giohang = Category.objects.all().filter(id__in=list(cart))
    sum_price = 0
    for p in giohang:
        p.total = cart.count(p.id)
        p.total_price = cart.count(p.id) * p.price
        sum_price = sum_price + p.total_price

    return render(request, "giohang.html", {'giohang': giohang, 'sum_price': sum_price})


def postgiohang(request):
    cart = (request.session['cart'])
    if request.method == "POST":
        # will add the object that they have posted to the card.
        # we called our form object input object ID . the input name = "obj_id"
        # after clicking to addToItem  => the item will add to cart by its porduct.id as value and obj_id as name in input
        # cart.append(int(request.POST['data']))
        data = json.loads(request.body)
        cart.append(int(data))
        request.session['cart'] = cart
        # catalog is the name of the main pagedata
    return HttpResponse(len(cart))


def updategiohang(request, cartcounter=None):
    cart = (request.session['cart'])
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        # while  data in cart:
        #     cart.remove(data)
        for key, value in data.items():
            if key == 'remove':  # xoa all cart
                while int(value) in cart:
                    cart.remove(int(value))
            if key == 'desc':  # desc cart
                cart.remove(int(value))
                request.session['cart'] = cart
                return HttpResponse(cart.count(int(value)))
            if key == 'inc':
                cart.append(int(value))
                request.session['cart'] = cart
                return HttpResponse(cart.count(int(value)))

        request.session['cart'] = cartcounter

    return HttpResponse(len(cart))


def sanpham(request, query):
    if not query:
        query = request.GET.get('query', '')
    sanpham = Category.objects.all().filter(slug=query)
    id_sp = sanpham.values('id')[0].get("id")
    image = Imageslide.objects.all()
    i = 0
    for p in image:
        p.counter = i
        i = i + 1
    # 'listimage': image
    return render(request, "sanpham.html", {'sanpham': sanpham, 'image': image})
