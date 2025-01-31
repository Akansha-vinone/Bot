from django.shortcuts import render,redirect,HttpResponse
from .models import Register
import json,os
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

Ques = [
        'How are You? ',
        "I want to know about you more!! What' Your Age?",
        "What's your favourite color?",
        "What's Your favourite movie?",
        "What You want to achieve in your Life",
        "what's Your hobby like Dancing,Singing,reading etc?",
        "Do You Know how to achieve Your goals like what will be your Path?",
        "What's your greatest acheivement till now ?",
        "Give a breif Family Intro",
        "What is your strength"
    ]

    
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Register.objects.get(email=email)
        except Register.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return render(request, 'login.html')

        if user.password == password:
            request.session['id'] = user.id  
            return redirect('chatBot')  
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'login.html')

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if not name or not email or not password:
            messages.error(request, "All fields are required!")
            return render(request, 'register.html')
        
        if password != confirm_password:
            messages.error(request,'Password should be Same in both fields.')
            return render(request,'register.html')
        
        user = Register(
            name = name,
            email = email,
            password = password
        )
        user.save()
        return render(request, 'login.html')
    
    else:
        return render(request,'register.html')
 
def chatBot(request):
    user_id = request.session.get('id')
    if not user_id:
        return redirect('login')

    if 'responses' not in request.session:
        request.session['responses'] = {}
    if 'ques_idx' not in request.session:
        request.session['ques_idx'] = 0

    responses = request.session['responses']  
    ques_idx = request.session['ques_idx']  

    if request.method == 'POST':
        answer = request.POST.get('answer')
        if ques_idx < len(Ques) and answer:
            current_question = Ques[ques_idx]  
            responses[current_question] = answer  
            request.session['responses'] = responses  

            ques_idx += 1 
            request.session['ques_idx'] = ques_idx  

            if ques_idx == len(Ques):  
                stored_data(user_id, responses)
                request.session['responses'] = {}  
                request.session['ques_idx'] = 0
                return redirect('Thankyou')

    if ques_idx < len(Ques):
        current_question = Ques[ques_idx]
    else:
        current_question = None

    context = {
        'current_question': current_question,
        'responses': responses,  
    }
    return render(request, 'chat.html', context)



def stored_data(user_id, responses):
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'user_data.json')

    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump([], file)  

    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []  
    user_data = {
        "user_id": user_id,
        "responses": responses,
    }
    data.append(user_data)

    with open(file_path, 'w') as file:
        json.dump(data, file)

def Thankyou(request):
    return render(request,'Thankyou.html')


def forgetPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        print(email)
        if Register.objects.filter(email = email).exists:
            user = Register.objects.get(email = email)
            print("Users Exist")
            send_mail("Reset Your password !",
                      f"hey, {user} Reset your password by click the link below :\n\n http://127.0.0.1:8000/newPasswordPage/{user}",
                      settings.EMAIL_HOST_USER,[email],
                      fail_silently=True)
            return HttpResponse("""YOUR link is send to your registered mail Id. \n
                                Please check and Reset your password.\n\n\n
                                
                                
                                We are waiting For You
                                """)
        else:

            return render(request,'forget_password.html')
    return render(request,'forget_password.html')

def NewPasswordPage(request,user):
    user_id = Register.objects.get(name = user)
    if request.method == 'POST':
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')   
        print("Pass1 and Pass2 :",pass1,pass2)

        if pass1 == pass2:
            user_id.set_password(pass1)
            user_id.save()
            return HttpResponse("Your password is Reset Successfully!!")
    return render(request,'new_password.html',{'user': user_id,'user_name':user_id.name})

