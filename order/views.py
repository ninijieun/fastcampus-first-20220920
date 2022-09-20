from time import timezone
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from order.models import Shop,Menu,Order,Orderfood
from order.serializers import ShopSerializer,MenuSerializer

# Create your views here.
@csrf_exempt
def shop(request):
    if request.method =='GET':
        # shop = Shop.objects.all()
        # serializer = ShopSerializer(shop, many=True) #JSON형태로 변경처리.
        # return JsonResponse(serializer.data, safe=False)

        shop = Shop.objects.all()
        return render(request,'order/shop_list.html',{'shop_list':shop})
    
    elif request.method == 'POST': #수정
        data = JSONParser().parse(request)
        serializer = ShopSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400) 

@csrf_exempt
def menu(request,shop):
    if request.method =='GET':
        menu = Menu.objects.filter(shop=shop)
        # serializer = MenuSerializer(menu, many=True) #JSON형태로 변경처리.
        # return JsonResponse(serializer.data, safe=False)
        return render(request,'order/menu_list.html',{'menu_list':menu,'shop':shop})
    
    elif request.method == 'POST': #수정
        data = JSONParser().parse(request)
        serializer = MenuSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

from django.utils import timezone
@csrf_exempt
def order(request):
    if request.method == 'POST':
        address = request.POST['address']
        shopId = request.POST['shopId']
        order_date = timezone.now()
        food_list = request.POST.getlist('menu')

        shop_item = Shop.objects.get(pk=int(shopId))

        shop_item.order_set.create(address=address,order_date=order_date,shop=int(shopId)) 
        
        order_item = Order.objects.get(pk = shop_item.order_set.latest('id').id)
        for food in food_list:
            order_item.orderfood_set.create(food_name = food)

        return render(request,'order/success.html')

    elif request.method == 'GET':
        order_list = Order.objects.all()
        return render(request,'order/order_list.html',{'order_list':order_list})
