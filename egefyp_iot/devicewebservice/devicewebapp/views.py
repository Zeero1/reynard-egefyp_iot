from django.shortcuts import render, redirect
import pymongo
import json

from devicewebapp.mqttdev import xdata, ydata, motor_on

"""Uncomment - required for UserLogin/Registration Page"""
from devicewebapp.forms import UserForm,UserProfileInfoForm

"""Uncomment all rest_framework lib - required for REST Token Authentication Page"""
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

#import socketio

from datetime import datetime as dt

"""Uncomment - required for UserLogin/Registration Page Authentication and Access"""
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt
#from django.contrib import messages
# import nmap
import subprocess
import re

from django.contrib import messages



def command_view(request):
    return render(request,'devicewebapp/macaddresses.html',context={})

# Create your views here.
def index(request):
    return render(request,'devicewebapp/index.html')

@login_required
def viewdevices(request):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["UIOT"]
    mycol = mydb["Devices"]
    devconncol = mydb["DeviceConns"]

    viewdevices = []
    viewdeviceconns = []

    for device in mycol.find():
        viewdevices.append(device)

    for devconns in devconncol.find():
        viewdeviceconns.append(devconns)
        print(devconns)

    devdata = {'viewdevicesdata': viewdevices, 'viewdeviceconndata':viewdeviceconns}
    return render(request,'devicewebapp/viewdevices.html',context=devdata)

# uncomment to enable token authentication
@api_view()
@permission_classes([IsAuthenticated])
def devices(request,param1):

    dev_name = param1
    dtnow = dt.now()

    iotdev = { "name": dev_name, "datetime": dtnow }

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["UIOT"]
    mycol = mydb["Devices"]
    devconncol = mydb["DeviceConns"]

    viewdevices = []
    for device in mycol.find({'name':dev_name}):
        viewdevices.append(device)

    if (len(viewdevices) >= 1):
        iotdevlog={ "name": dev_name, "datetime": dtnow, "status":"updated" }
        y = devconncol.insert_one(iotdevlog)
        dev_name = "{} updated in DB".format(dev_name)
    else:
        x = mycol.insert_one(iotdev)
        iotdevlog={ "name": dev_name, "datetime": dtnow, "status":"new" }
        y = devconncol.insert_one(iotdevlog)
        dev_name = "{} device has been recorded!!".format(dev_name)

    # 'user': str(request.user)
    # 'auth': str(request.auth)
    print('\'user\':{}\n\'auth\':{}\n'.format(str(request.user), str(request.auth)))
    # return render(request, 'devicewebapp/devices.html', context={'data': dev_name})
    return render(request, 'devicewebapp/devices.html', context={'data': iotdev, 'datalog': iotdevlog, 'msg_display': res_dev_name})

#Postview function Not used for EG284S
@csrf_exempt
def postview(request):
    if request.method == 'POST':
        usrname = request.POST.get('username')
        passwd = request.POST.get('password')
        print("HTTP-POST: username:{} and password:{}".format(usrname,passwd))
        return HttpResponse("POST Request data {} with {} sent- successful".format(usrname,passwd))

    elif request.method == 'GET':
        if request.GET.get('username',''):
            usrname = request.GET.get('username','')
            access_token=request.GET.get('token','')
            if access_token != "":
                print("username:{} | token:{} - HTTP-GET successful".format(usrname,access_token))
                response_data = {"username": usrname, "token received": access_token}
            else:
                print("username:{} - HTTP-GET successful".format(usrname))
                response_data = {"username": usrname, "time queried": dt.now().strftime("%d-%m-%Y %H:%M:%S")}
            return JsonResponse(response_data)
            #return HttpResponse("Request {} exist with {} - HTTP-GET successful".format(usrname,passwd))
        else:
            qstring=request.GET.get('search','')
            print("HTTP-GET: query string:{}".format(qstring))
            return HttpResponse("HTTP-GET: Query Done - {}".format(qstring))

    else:
        print("Error - Request is Invalid {}".format(request))
        return HttpResponse("Request {} with {} - HTTP-GET error in data".format(usrname,passwd))


def messageview(request):
    getydata=""
    getxdata=0

    #data received from mqttdev.py module
    print("xdata:{}".format(xdata))
    print("ydata:{}".format(ydata))

    #data received from mqttdev.py module assigned to local variable to be passed to html
    getxdata=xdata
    getydata=ydata
    print("getxdata:{}".format(getxdata))
    print("getydata:{}".format(getydata))

    return render(request,'devicewebapp/messageview.html',context={'yetdata':getydata,'getdata': getxdata})

def activatemotorview(request):
    # import function to run
    #from path_to_script import function_to_run
    # call function
    #function_to_run()
    # return user to required page
    if request.method == 'POST' and 'activate' in request.POST:
        print("Run script request received {}".format(request.POST.get('activate')))
        activate_value=request.POST.get('activate')
        print("Activate:{}".format(activate_value))
        motor_on(activate_value)
    elif request.method == 'POST' and 'deactivate' in request.POST:
        print("Run script request received {}".format(request.POST.get('deactivate')))
        activate_value=request.POST.get('deactivate')
        print("Dectivate:{}".format(activate_value))
        motor_on(activate_value)
    return HttpResponseRedirect(reverse(messageview))

#uncomment register function

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'devicewebapp/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})


# Authenticate (was commnented)
@api_view()
@permission_classes([IsAuthenticated,])
def hello(request):
    print("Request Data-Content (params)\n{}\n".format(request.content_type))
    print("Request Data-Content (body)\n{}".format(request.body))
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    return Response(content,template_name='devicewebapp/hello.html')
    #return HttpResponse(request,'devicewebapp/hello.html',{content})
# 

#uncomment user_loggedin function

def user_loggedin(request):
    return(request,'devicewebapp/index.html')


#uncomment user_logout function

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


#uncomment user_login function

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)
        # If we have a user
        if user:
            #Check it the account is active
            print("user logged in")
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))

            messages.success(request, ('Invalid login details supplied.'))
            # return render(request, 'devicewebapp/login.html', {})
            return redirect('devicewebapp/login.html')
            # return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'devicewebapp/login.html', {})
