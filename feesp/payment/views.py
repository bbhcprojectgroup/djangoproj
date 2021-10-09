from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
#from .models import Transaction
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
from login.views import encrypt
from login.models import Account
from examfee.views import data_save
from .models import Transaction
from acdfee.views import saveacad, clgfee
import random, string

@csrf_exempt
def initiate_payment(request):
    """if request.method == "GET":
        return render(request, 'payments/pay.html')"""
    """try:
        username = request.POST['username']
        password = request.POST['password']
        amount = int(request.POST['amount'])
        if(Account.objects.filter(username=username).exists()):
                 user = Account.objects.get(username=username)

        if user is None:
            raise ValueError
        #auth_login(request=request, user=user)
    except:
            return render(request, 'payments/pay.html', context={'error': 'Wrong Accound Details or amount'})"""


    amount=request.POST['amt']
    global work
    work=request.POST['type']
    print(work)
    user=request.user
    #if (user.check_password(password)):
    """transaction = Transaction.objects.create(made_by=user, amount=int(float(amount)))
    transaction.save()"""
    merchant_key = settings.PAYTM_SECRET_KEY
    global usr
    usr=request.user
    order_id='FEEPAY_'+''.join(random.choice(string.digits) for x in range(5)) 
    while(Transaction.objects.filter(order_id=order_id).exists()):
         order_id='FEEPAY_'+''.join(random.choice(string.digits) for x in range(5))

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(order_id)),
        ('CUST_ID', str(user.email)),
        ('TXN_AMOUNT', str(amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    """transaction.checksum = checksum
    transaction.save()"""

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'payments/redirect.html', context=paytm_params)
    """else:
        return render(request, 'payments/pay.html', context={'error': 'Wrong Password'})"""

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        login(request, usr)
        print("logged in")

        print(request.user)
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if(Transaction.objects.filter(made_by=usr,status="FAILED",payment_type=work).exists()):
            old_data=Transaction.objects.get(made_by=usr,status="FAILED",payment_type=work)
            old_data.delete()
        if(work == 'examfee'):
                
                received_data['exam']='True'
                
        else:
                
                received_data['exam']='False'
               
 
        if(received_data['RESPMSG']==['Txn Success']):
            status="SUCCESS"
            received_data['succ']='True'
            if(work == 'examfee'):
                
                data_save(request,received_data['ORDERID'][0])
                
            else:
                
                saveacad(request,received_data['ORDERID'][0])
        else:
            status="FAILED"        
            print(":)")
        transaction = Transaction.objects.create(made_by=usr, amount=int(float(received_data['TXNAMOUNT'][0])),order_id=received_data['ORDERID'][0],payment_type=work,checksum=received_data['CHECKSUMHASH'][0],status=status,user_mail=usr.email)
        transaction.save()
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'payments/callback.html', context=received_data)
        return render(request, 'payments/callback.html', context=received_data)

