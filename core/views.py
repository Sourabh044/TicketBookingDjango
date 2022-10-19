from site import makepath
from django.http import HttpResponse
from django.shortcuts import render
from datetime import date, datetime , timedelta
from random import Random
from time import time
from .util import send_email_token, send_reset_otp
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate , views , get_user_model  
User = get_user_model()
# Create your views here.
 

def HomePage(request):
        return render(request, 'base.html')


def otpexpire(user):
    time = datetime.now().astimezone()-user.updated_at.astimezone()
    total_seconds = time.total_seconds() 
    minutes = total_seconds/60
    print(minutes)
    if(minutes>5):
        return True
    else:
        return False

def genOtp(user):
    import random
    user.otp = random.randint(1000,9999)
    print(user.otp)
    user.save()
    return user.otp

# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)

#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }

# Create your views here.

# All User Views Here.  

def UserLogin(request):
        if request.method  == 'POST':
                try:
                   email = request.POST['email']
                   password = request.POST['password']
                   user = authenticate(email=email, password=password)
                   if user is not None:
                        if not user.is_verified:
                                print('Updated_at',user.updated_at.astimezone(),'\nTime now',datetime.now().astimezone())
                                if otpexpire(user):
                                        otp = genOtp(user)
                                        send_email_token(user.otp,user.email)
                                        return HttpResponse('otp Expired New Otp Sent.')
                                        import random
                                otp = genOtp(user)
                                send_email_token(user.otp,user.email)
                                return HttpResponse({
                                'status': True,
                                'info': 'Verify_user',
                                'msg':'An otp send to your registered email.',
                                'is_verified': user.is_verified,
                                })
                        return HttpResponse({
                                'status': True,
                                'message': 'login Successfully',
                                'is_verified': user.is_verified,
                        })
                   return HttpResponse({
                        'status': False,
                        'message': 'Invalid username and password'
                })
                except Exception as e:
                        print(e)
                        return HttpResponse({
                                'status': False,
                                'message': "something went wrong"
                        })
        return HttpResponse('login page Here')
                


def signup(self, request):
    if request.method == 'POST':
        print(request.data)
        try:
            if not request.user.is_anonymous:
                return HttpResponse({
                    'error': False,
                    'message': "Not Allowed"
                })
            if request.method  == 'POST':
                username = request.POST['username']
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                email = request.POST['email']
                # password = request.POST['phone']
                password = request.POST['password']
                password = make_password(password)
                newuser = User.objects.create_user(username = username , password = password, email=email,first_name= first_name, last_name= last_name) # 
                newuser.save()
        except Exception as e:
                print(e)
                return HttpResponse(e)
    return HttpResponse('Signup page Here')
    

def UserVerifyView(request):
        id = request.user.id
        user = User.objects.get(id=id)
        if user.is_verified==True:
            otp = genOtp(user)
            print('newotp',otp)
            return HttpResponse({
                'status': False,
                'msg': 'already verified'
            })
        data = request.data
        try:
            try:
                print(user,'initial otp:',user.otp)
                dataotp = (data['otp'])
                print(type(dataotp['otp']))
                if int(dataotp['otp']) == user.otp:
                        if otpexpire(user):
                            otp = genOtp(user)
                            send_email_token(user.otp,user.email)
                            return HttpResponse({
                                'status' :False,
                                'info': 'OTP Expired',
                                'msg': 'Request OTP',
                            })                            
                        otp = genOtp(user)
                        data['is_verified'] = True
                        data['otp'] = otp
                        user.is_verified =True
                        user.save()
                        # serializer = Htt(user,data=data, partial=True)
                        # serializer.is_valid(raise_exception=True)
                        # print(serializer.validated_data.get('otp'))
                        print('updating user')
                        # serializer.save()
                        return HttpResponse({
                        'msg' : 'bhai tera otp match hogya',
                        "status": True
                        })
                else:
                    return HttpResponse({
                        'status' : False,
                        'msg' : 'Invalid OTP'
                    })
            except Exception as e:
                return HttpResponse({
                'status' : False,
                'mag':e
                })
        except Exception as e:
            print(e)
            return HttpResponse({
            'status' : False,
            'error':e
        })

def UserProfileView(request, pk=None):
        user = request.user
        return HttpResponse({
            'status':True,
            "msg":user.values(),
            'verification':request.user.is_verified
        })

def UserPasswordChange(request):
        data = request.data
        id = request.user.id
        if 'password' in data:
            user = User.objects.get(id=id)
            print(user)
            if not user.is_verified:
                return HttpResponse({
                    'status' : False,
                    'msg': 'User is not verified',
                })
            password = request.data.get('password')
            print('Request data:',request.data)
            user = make_password(password)
            user.set_password(password)
            user.save()
            return HttpResponse({
                'status' : True,
                'msg': 'User Password has changed.'           
            })
        return HttpResponse({
            'status': False,
            "msg":'provide password'
        })



# Mail to send if the user password has been forgot
# def UserPasswordResetMail(request):

#         try:
#             serializer = UserPasswordResetMailSerializer(data=request.data)
#             if serializer.is_valid(raise_exception=True):
#                 return Response({
#                     'msg':'An Email Has been sent on your email'
#                 })
#         except Exception as e:
#             return Response({
#                 'msg':'error occured',
#                 'errors': e
#             })

def UserPasswordReset(request):
        data = request.data
        email = request.data['email']
        user = User.objects.get(email=email)
        if 'otp' in data:
            try:
                if int(data['otp']) == user.otp:
                    user.password = make_password(data['password'])
                    otp = genOtp(user)
                    return HttpResponse({
                        'status' : True,
                        'msg': 'New Password Set.'           
                    })
                return HttpResponse({
                    'status' : False,
                    'msg': 'Invalid OTP'
                })
            except Exception as e:
                    print(e)
                    return HttpResponse({
                    'status' : False,
                    'msg': e
                })
        return HttpResponse({
            'status' : False,
            'msg': 'Provide OTP'
        })

