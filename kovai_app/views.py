from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests
from .models import TutorRequest,TutorRegistration,Requestpost,Message,teacher_addcard, student_addcard,Transaction
from django.core.mail import send_mail , message,EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import random
from twilio.rest import Client
from urllib.parse import parse_qs
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.contrib import messages
from django.contrib.auth.decorators import login_required
import uuid

# Create your views here.
def mains(request):
    return render(request,"new_home.html")
def tutor_request(request):
    if request.method=="POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        location = request.POST.get("location")
        phone = request.POST.get("phone")
        password=request.POST.get("password")
        gender=request.POST.get("gender")
        

        if TutorRequest.objects.filter(email=email).exists():
           return render(request, 'request_tutor.html',{"msg":"An account with this email already exists."})
        else:
    
            print("jjvv")
# Generate a random 6-digit OTP
            otp = random.randint(100000, 999999)


            logins={"otp":otp}
            html_template="otp.html"
            html_message=render_to_string(html_template,logins)
        
            email_from=settings.EMAIL_HOST_USER
            r_list=[email]
            subject="Verification Otp"
            message=EmailMessage(subject,html_message,email_from,r_list)
            message.content_subtype='html'
            message.send()
            cote= random.randint(100000, 999999)
            uname=f'{name}{cote}'
            
            
            if User.objects.filter(email=email).exists():
                print("jj")
                return render(request, 'request_tutor.html',{"msg":"An account with this email already exists."})
            user = User.objects.create_user(username=uname, email=email, password=password)
            user = authenticate(request, username=email , password=password)  # Authenticate using email
            if user is not None:
                login(request, user)
            

            TutorRequest.objects.create(
                user=user,
                name=name,
                email=email,
                location=location,
                phone=phone,
               
                mobile_otp=otp,
                password=password,
                gender=gender
            )
            logins={"name":name,"email":email,"password":password,"msg":"Otp sented to your Register Email Number to verify your Account"}
            # html_template="a_email_verify.html"
            # html_message=render_to_string(html_template,login)
        
            # email_from=settings.EMAIL_HOST_USER
            # r_list=[email]
            # subject="Action required: Please confirm to post requirement"
            # message=EmailMessage(subject,html_message,email_from,r_list)
            # message.content_subtype='html'
            # message.send()

            print(otp)
            
            return render(request, 'otp_verfication_student.html',logins)
        


        
        
        # Validate the data if necessary
        
        # Save the data to the database
       
    
    return render(request, 'request_tutor.html')

def otp_verify(request,email):
    if request.method=="POST":
        otp=request.POST.get("otp")
        print(type(otp),otp)
        s=TutorRequest.objects.filter(email=email).first()
        print("m",type(s.mobile_otp),s.mobile_otp)
        print(s.mobile_otp==int(otp))
        if int(s.mobile_otp)==int(otp):
            return render(request,"addpost.html",{"name":s.name,"email":email})
        else:
            return render(request, 'otp_verfication_student.html',{"name":s.name,"email":email,"msg":"Otp is incorrect"})
            

def addpost(request,email):
    student = TutorRequest.objects.filter(email=email).first()
    if request.method=="POST":
        classes=request.POST.get("classes")
        cariculam=request.POST.get("curriculum")
        dyr = request.POST.get("dyr")
       
        subject = request.POST.get("subject")
        two_subject = request.POST.get("two_subject")
        three_subject = request.POST.get("three_subject")
        four_subject=request.POST.get("four_subject")
        five_subject=request.POST.get("five_subject")
        i_want = request.POST.get("i_want")
        meeting_option= request.POST.get("meeting_option")
        budget = request.POST.get("budget")
        budget_need = request.POST.get("budget_need")
        
        language = request.POST.get("language")
        
        need = request.POST.get("need")
        
        gender = request.POST.get("gender")
        image = request.FILES.get('image')
        l=TutorRequest.objects.filter(email=email).first()
        if image:
            Requestpost.objects.create( 
            email=email,
            curriculum=cariculam,
            classes=classes,
            dyr=dyr,
            
            subject=subject,
            two_subject=two_subject,
            three_subject=three_subject,
            four_subject=four_subject,
            five_subject=five_subject,
            i_want=i_want,
            meeting_option=meeting_option,
         
            budget=budget,
            budget_need=budget_need,
            gender=gender,
            language=language,
           
            need=need,

            imagess=image,
           
            location=l.location,
            count=0
            )
        else:
             Requestpost.objects.create( 
            email=email,
            curriculum=cariculam,
            classes=classes,
            dyr=dyr,
            
            subject=subject,
            two_subject=two_subject,
            three_subject=three_subject,
            four_subject=four_subject,
            five_subject=five_subject,
            i_want=i_want,
            meeting_option=meeting_option,
         
            budget=budget,
            budget_need=budget_need,
            gender=gender,
            language=language,
           
            need=need,

            imagess=image,
           
            location=l.location,
             count=0
            )

        post = Requestpost.objects.filter(email=email).values
        student = TutorRequest.objects.filter(email=email).first()
        html_template="wellcome_mail.html"
        html_message=render_to_string(html_template,{"all":post,"post":student})
        email_from=settings.EMAIL_HOST_USER
        r_list=[email]
        subject="Action required: Please confirm to post requirement"
        message=EmailMessage(subject,html_message,email_from,r_list)
        message.content_subtype='html'
        message.send()
        #---
        tutor_list=[]
        tutor=TutorRegistration.objects.all()
        need_subject="none"
        for i in tutor:
            if i.subject and subject in i.subject:
                tutor_list.append(i.email)
                need_subject=subject
            elif two_subject:
                if i.subject and two_subject.capitalize() in i.subject:
                    tutor_list.append(i.email)
                    need_subject=two_subject
            elif three_subject:
                if i.subject and three_subject.capitalize() in i.subject:
                    tutor_list.append(i.email)
                    need_subject=three_subject
            
    
            elif four_subject:

                if i.subject and four_subject.capitalize() in i.subject:
                    eed_subject=four_subject
                    tutor_list.append(i.email)
            elif five_subject:
                if i.subject and five_subject.capitalize() in i.subject:
                    need_subject=five_subject
                    tutor_list.append(i.email)
            print(i.email)
            print(subject)
            print(meeting_option)
          
        

        messages.success(request, f"Welcome !! {student.name}")
        return redirect("myposts")

    return render(request,"addpost.html",{"name":student.name,"email":email})



def email_verify(request,email):
    
    return render(request, 'email_verifed.html',{"email":email})


#-----------------------my post-------------------------------------------------
@login_required
def myposts(request):
      user = request.user  # Get the logged-in user
      post = Requestpost.objects.filter(email=user.email).values
      print(post)
      student = TutorRequest.objects.filter(email=user.email).first()
      COIN_PACKS = [
    {"amount": 200, "label": "Starter Pack", "coins": 200, "bonus": 0, "total_coins": 200, "leads": 4, "effective_per_lead": 50},
    {"amount": 500, "label": "Basic Boost", "coins": 500, "bonus": 100, "total_coins": 600, "leads": 12, "effective_per_lead": 41.6},
    {"amount": 1000, "label": "Value Plus", "coins": 1000, "bonus": 250, "total_coins": 1250, "leads": 25, "effective_per_lead": 40},
    {"amount": 1500, "label": "Power User", "coins": 1500, "bonus": 400, "total_coins": 1900, "leads": 38, "effective_per_lead": 39.5},
    {"amount": 2000, "label": "Pro Pack", "coins": 2000, "bonus": 600, "total_coins": 2600, "leads": 52, "effective_per_lead": 38.5},
    {"amount": 3000, "label": "Ultimate Pack", "coins": 3000, "bonus": 900, "total_coins": 3900, "leads": 78, "effective_per_lead": 38.5},
]

      return render(request,"mypost.html",{"all":post,"post":student,"coin_packs":COIN_PACKS})



def delete_posst(request,id):
    post= Requestpost.objects.get(id=id)
    email=post.email
    post.delete()
    messages.success(request, f"deleted...")
    return redirect("myposts")
   

def mypost(request,email):
    post = Requestpost.objects.filter(email=email).order_by('-id')
    student = TutorRequest.objects.filter(email=email).first()
    return render(request,"mypost.html",{"all":post,"post":student})




# def stu_login(request):
#     if request.method=="POST":
#         email=request.POST.get('email')
#         password=request.POST.get('password')
#         student = TutorRequest.objects.filter(email=email).first()
#         print(student.password)
#         if TutorRequest.objects.filter(email=email,password=password).exists():
#             # post = Requestpost.objects.filter(email=email).values
#             # student = TutorRequest.objects.filter(email=email).first()
#             # return render(request,"mypost.html",{"all":post,"post":student})
#             return redirect("mypost", email=email)
           
#         else:
#             return render(request,"login.html",{"msg":"your login detail is wong"})
        



#     return render(request,"login.html")


import re  # For validating email

def stu_login(request):
    if request.method == "POST":
        identifier = request.POST.get('email')  # Could be email or phone number
        password = request.POST.get('password')
        login_type= request.POST.get('login_type')

       
        user = authenticate(request, username=identifier , password=password)  # Authenticate using email
        
        if user is not None:
           
            if login_type=="learner":
                if TutorRequest.objects.filter(email=identifier).exists():
                    login(request, user)
                    request.session.set_expiry(60 * 60 * 24 * 7)  # 7 days
                    return redirect("myposts")  # Redirect using the student's email
                else:
                    return render(request, "login.html", {"msg": "plase login with As tutor"})

            elif login_type=="tutor":
                if TutorRegistration.objects.filter(email=identifier).exists():
                    login(request, user)
                    request.session.set_expiry(60 * 60 * 24 * 7)  # 7 days
                    return redirect('teacher_dashboard')  # Redirect using the tutor's email
                else:
                    return render(request, "login.html", {"msg": "plase login with As learner"})
        else:
            return render(request, "login.html", {"msg": "Your login details are incorrect."})

    return render(request, "login.html")




def teacher_reg(request):
    if request.method == "POST":
       name = request.POST.get('name')
       email = request.POST.get('email')
       password = request.POST.get('password')
       confirm_password = request.POST.get('confirm_password')
       phone=request.POST.get("number")
       if TutorRegistration.objects.filter(email=email,password=password).exists():
           
          return render(request,"teacher_regs.html",{"msg":"your account  already exist"})
       elif User.objects.filter(email=email).exists():
            return render(request,"teacher_regs.html",{"msg":"your account   already exist"})
           
       else:
           cote= random.randint(100000, 999999)
           uname=f'{name}{cote}'
          
           user = User.objects.create_user(username=uname, email=email, password=password)
          
           TutorRegistration.objects.create(
               user=user,
                name=name,
                email=email,
                password=password,
                confirm_password=confirm_password,
                phone=phone
            )
           user = authenticate(request, username=email , password=password)  # Authenticate using email
           login(request, user)
           return redirect('details')
            
           
        #    ds={"name":name,"email":email,"msg":"Account created! Just a few more details to finalize your tutor profile."}

        #    return render(request, 'details.html', ds)
           
    
    return render(request, 'teacher_regs.html')

def  details(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            # Fetch user details
            
        
            tutor = TutorRegistration.objects.filter(email=request.user.email).first()

            # Generate OTP for email verification
            otp = random.randint(100000, 999999)
            print(otp)
            email_data = {"otp": otp}
            html_template = "otp.html"
            html_message = render_to_string(html_template, email_data)

            # Send OTP email
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]
            subject = "Verification OTP"
            message = EmailMessage(subject, html_message, email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()
            
            # Create tutor record in one go
            
                
            tutor.profile_description=request.POST.get('profile_description')
            
            tutor.id_proof=request.FILES.get('id_proof')
            tutor.profile_photo=request.FILES.get('profile')
            tutor.filename=f'images/{request.FILES.get("profile")}' if 'profile' in request.FILES else None
            tutor.email_otp=otp
            tutor.company_name=request.POST.get('company_name')
            tutor.job_roll=request.POST.get('job_roll')
            tutor.year_of_experience=request.POST.get('year_of_experience')
            tutor.company_name_two=request.POST.get('company_name_two')
            tutor.job_roll_two=request.POST.get('job_roll_two')
            tutor.year_of_experience_two=request.POST.get('year_of_experience_two')
            tutor.company_name_three=request.POST.get('company_name_three')
            tutor.job_roll_three=request.POST.get('job_roll_three')
            tutor.year_of_experience_three=request.POST.get('year_of_experience_three')
            tutor.company_name_four=request.POST.get('company_name_four')
            tutor.job_roll_four=request.POST.get('job_roll_four')
            tutor.year_of_experience_four=request.POST.get('year_of_experience_four')
            tutor.company_name_five=request.POST.get('company_name_five')
            tutor.job_roll_five=request.POST.get('job_roll_five')
            tutor.year_of_experience_five=request.POST.get('year_of_experience_five')
            tutor.institution_name=request.POST.get('institution_name')
            tutor.degree_type=request.POST.get('degree_type')
            tutor.degree_name=request.POST.get('degree_name')
            tutor.specialisation=request.POST.get('specialisation')
            tutor.institution_name_two=request.POST.get('institution_name_two')
            tutor.degree_type_two=request.POST.get('degree_type_two')
            tutor.degree_name_two=request.POST.get('degree_name_two')
            tutor.specialisation_two=request.POST.get('specialisation_two')
            tutor.institution_name_three=request.POST.get('institution_name_three')
            tutor.degree_type_three=request.POST.get('degree_type_three')
            tutor.degree_name_three=request.POST.get('degree_name_three')
            tutor.specialisation_three=request.POST.get('specialisation_three')
            tutor.institution_name_four=request.POST.get('institution_name_four')
            tutor.degree_type_four=request.POST.get('degree_type_four')
            tutor.degree_name_four=request.POST.get('degree_name_four')
            tutor.specialisation_four=request.POST.get('specialisation_four')
            tutor.institution_name_five=request.POST.get('institution_name_five')
            tutor.degree_type_five=request.POST.get('degree_type_five')
            tutor.degree_name_five=request.POST.get('degree_name_five')
            tutor.specialisation_five=request.POST.get('specialisation_five')
            
            tutor.from_level=request.POST.get('level')
            
            tutor.min_fee=request.POST.get('min_fee')
            tutor.max_fee=request.POST.get('max_fee')
            tutor.classes=request.POST.get('classes')
            tutor.curriculum=request.POST.get('curriculum')
            tutor.language_subject=request.POST.get('language_subject')
            tutor.other_subject=request.POST.get('other_subject')
            tutor.willing_to_travel=request.POST.get('willing_to_travel')
            tutor.available_for_online_teaching=request.POST.get('available_for_online_teaching')
            tutor.help_with_homework=request.POST.get('homework')
            tutor.full_time_teacher=request.POST.get('full_time')
            tutor.interested_in=request.POST.get('interested_in')
            #tutor.types = request.POST.get('types')
            tutor.strength = request.POST.get('strength')
            tutor.gender = request.POST.get('gender')
            tutor.date_of_birth = request.POST.get('dates')
            tutor.location = request.POST.get('location')
            tutor.language = request.POST.get('lanquage')
            if request.POST.get('subject'):
                tutor.subject = request.POST.get('subject').split(",")

            tutor.i_charge = request.POST.get('i_charge')
            tutor.save()

            # print(request.POST.get('subject').split(","))
            # print(tutor.subject)
        
            # Success message
            ds = {"name": tutor.name, "email": tutor.email, "msg": "Tutor registration completed successfully"}
            return render(request,"otp_verfication_teachet.html",ds)

        return render(request, 'details.html')
    return render(request,"new_home.html")


# def details(request,email):
#     print(email)
#     if request.method == "POST":
#         types = request.POST.get('types')
#         strength = request.POST.get('strength')
#         gender = request.POST.get('gender')
#         date_of_birth = request.POST.get('dates')
#         location = request.POST.get('location')
#         language = request.POST.get('lanquage')
#         language_two = request.POST.get('lanquage_2')
#         language_three = request.POST.get('lanquage_3')
#         language_four = request.POST.get('lanquage_4')
#         language_five = request.POST.get('lanquage_5')

#         post_code = request.POST.get('post_code')

#         #  # Example: using session to get the tutor id
#         tutor = TutorRegistration.objects.filter(email=email).first()

#         # Update the tutor details
#         tutor.types = types
#         tutor.strength = strength
#         tutor.gender = gender
#         tutor.date_of_birth = date_of_birth
#         tutor.location = location
#         tutor.language=language
#         if language_two:
#             tutor.language_two=language_two
#         if language_three:
#             tutor.language_three=language_three
#         if language_four:
#             tutor.language_four=language_four
#         if language_five:
#             tutor.language_five=language_five
#         tutor.post_code = post_code
#         tutor.save()
#         msg="you personal detail has saved"
#         ds={"name":tutor.name,"email":tutor.email,"msg":msg}
#         return render(request, 'subject.html',ds)

  
  

#subject

def subject(request,email):
    if request.method == "POST":
        lsubject = request.POST.get('subjects')
        llevel = request.POST.get('level')
        level=""
        print(lsubject,"this is subject")
        if lsubject :
            subject=lsubject.split(",")
            #level=llevel.split(",")
            print(subject,level)
        tutor = TutorRegistration.objects.filter(email=email).first()
        if tutor:
            # Update the tutor details from the POST data
            tutor.subject = subject
            tutor.from_level=level
           
           

            # Save the updated details
            tutor.save()

            # Prepare the data to be passed to the next template
            ds = {"name": tutor.name, "email": tutor.email,"msg":"successfully save your subject"}
            return render(request, 'eduction.html',ds)
    return render(request, 'subject.html',{"email":email})
# add ....subject

def addsubject(request,email):
    if request.method == "POST":
        subject = request.POST.get('subject')
        level = request.POST.get('level')
        to_level = request.POST.get('to_level')
        tutor = TutorRegistration.objects.filter(email=email).first()
        name = tutor.name
        email = tutor.email
        password = tutor.password
        TutorRegistration.objects.create(name=name,email=email,password=password,subject=subject,from_level=level,to_level=to_level)
        ds={"name":name,"email":email,"msg":"successfully saved your "}
        return render(request,"eduction.html",ds)
    


#add cerficate

def certificate(request, email):
    tutor = TutorRegistration.objects.filter(email=email).first()
    ds={"name":tutor.name,"email":tutor.email,"msg":"your subject saves"}
    if request.method == "POST":
        # Get data from POST request
        institution_name = request.POST.get('institution_name')
        degree_type = request.POST.get('degree_type')
        degree_name = request.POST.get('degree_name')
        specialisation= request.POST.get('specialisation')
        institution_name_two = request.POST.get('institution_name_two')
        degree_type_two = request.POST.get('degree_type_two')
        degree_name_two = request.POST.get('degree_name_two')
        institution_name_three = request.POST.get('institution_name_three')
        degree_type_three = request.POST.get('degree_type_three')
        degree_name_three = request.POST.get('degree_name_three')
        institution_name_four = request.POST.get('institution_name_four')
        degree_type_four = request.POST.get('degree_type_four')
        degree_name_four = request.POST.get('degree_name_four')
        institution_name_five = request.POST.get('institution_name_five')
        degree_type_five = request.POST.get('degree_type_five')
        degree_name_five= request.POST.get('degree_name_five')

        specialisation_two= request.POST.get('specialisation_two')
        specialisation_three= request.POST.get('specialisation_three')
        specialisation_four= request.POST.get('specialisation_four')
        specialisation_five= request.POST.get('specialisation_five')
       

        # Fetch the tutor based on the email
        tutor = TutorRegistration.objects.filter(email=email).first()

        if tutor:
            # Update the tutor details
            tutor.institution_name = institution_name
            tutor.degree_type = degree_type
            tutor.degree_name = degree_name
            tutor.institution_name_two=institution_name_two
            tutor.degree_type_two=degree_type_two
            tutor.degree_name_two=degree_name_two
            tutor.institution_name_three=institution_name_three
            tutor.degree_type_three=degree_type_three
            tutor.degree_name_three=degree_name_three
            tutor.institution_name_four=institution_name_four
            tutor.degree_type_four=degree_type_four
            tutor.degree_name_four=degree_name_four
            tutor.institution_name_five=institution_name_five
            tutor.degree_type_five=degree_type_five
            tutor.degree_name_five=degree_name_five
            tutor.specialisation=specialisation
            tutor.specialisation_two=specialisation_two
            tutor.specialisation_three=specialisation_three
            tutor.specialisation_four=specialisation_four
            tutor.specialisation_five=specialisation_five



            tutor.save()

            ds={"name":tutor.name,"email":tutor.email,"msg":"your  Education saves"}

            # Redirect to a success page or another step
            return render(request, 'company_emp.html', ds)
    return render(request,"eduction.html",ds)


    # If GET request, just render the form template

def addcertificate(request, email):
    tutor = TutorRegistration.objects.filter(email=email).first()
    name=tutor.name
    email=tutor.email
    password=tutor.password
    ds={"name":tutor.name,"email":tutor.email,"msg":"your  Education saves"}
    if request.method == "POST":
        # Get data from POST request
        institution_name = request.POST.get('institution_name')
        degree_type = request.POST.get('degree_type')
        degree_name = request.POST.get('degree_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        association = request.POST.get('association')

        # Fetch the tutor based on the email
        tutor = TutorRegistration.objects.filter(email=email).first()
        name=tutor.name
        email=tutor.email
        password=tutor.password
        TutorRegistration.objects.create(name=name,email=email,password=password,institution_name=institution_name,degree_type=degree_type,degree_name=degree_name,start_date=start_date,end_date=end_date,association=association)

        
          

        ds={"name":tutor.name,"email":tutor.email,"msg":"your  Education saves"}

            # Redirect to a success page or another step
        return render(request, 'company_emp.html', ds)   
    return render(request, 'company_emp.html', ds)

def company_emp(request,email):
    tutor = TutorRegistration.objects.filter(email=email).first()
    name=tutor.name
    email=tutor.email
    password=tutor.password
    ds={"name":tutor.name,"email":tutor.email,"msg":"your education is saved"}
    if request.method=="POST":
          company_name=request.POST.get('company_name')
          job_roll=request.POST.get('job_roll')
          
          year_of_experience=request.POST.get('year_of_experience')

          company_name_two=request.POST.get('company_name_two')
          job_roll_two=request.POST.get('job_roll_two')
          
          year_of_experience_two=request.POST.get('year_of_experience_two')

          company_name_three=request.POST.get('company_name_three')
          job_roll_three=request.POST.get('job_roll_three')
          year_of_experience_three=request.POST.get('year_of_experience_three')

          company_name_four=request.POST.get('company_name_four')
          job_roll_four=request.POST.get('job_roll_four')
          
          year_of_experience_four=request.POST.get('year_of_experience_four')

          company_name_five=request.POST.get('company_name_five')
          job_roll_five=request.POST.get('job_roll_five')
          
          year_of_experience_five=request.POST.get('year_of_experience_five')

          tutor = TutorRegistration.objects.filter(email=email).first()
          tutor.company_name=company_name
          tutor.job_roll=job_roll
          tutor.year_of_experience=year_of_experience

          tutor.company_name_two=company_name_two
          tutor.job_roll_two=job_roll_two
          tutor.year_of_experience_two=year_of_experience_two

          tutor.company_name_three=company_name_three
          tutor.job_roll_three=job_roll_three
          tutor.year_of_experience_three=year_of_experience_three

          tutor.company_name_four=company_name_four
          tutor.job_roll_four=job_roll_four
          tutor.year_of_experience_four=year_of_experience_four

          tutor.company_name_five=company_name_five
          tutor.job_roll_five=job_roll_five
          tutor.year_of_experience_five=year_of_experience_five

        #   tutor.job_start_date=start_date
        #   if end_date:
        #       tutor.job_end_date=end_date
          tutor.save()
          ds={"name":tutor.name,"email":tutor.email}
          return render(request,'teaching_detail.html',ds)
    return render(request, 'company_emp.html', ds)

def teaching_detail(request, email):
    if request.method == "POST":
        # Retrieve the data from the POST request
        i_charge = request.POST.get('i_charge')
        min_fee = request.POST.get('min_fee')
        max_fee = request.POST.get('max_fee')
        classes = request.POST.get('classes')
        other_subject = request.POST.get('other_subject')
        curriculum = request.POST.get('curriculum')
        language_subject=request.POST.get('language_subject')
        travel = request.POST.get('travel')
        online_teach = request.POST.get('online_teach')
        homework = request.POST.get('homework')
        full_time = request.POST.get('full_time')
        interested_in = request.POST.get('interested_in')

        # Fetch the tutor record based on the email
        tutor = TutorRegistration.objects.filter(email=email).first()

        if tutor:
            # Update the tutor's details with the form data
            tutor.i_charge = i_charge
            tutor.min_fee = min_fee
            tutor.max_fee = max_fee
            tutor.classes = classes
            tutor.curriculum = curriculum
            tutor.language_subject = language_subject
            tutor.other_subject=other_subject
            tutor.willing_to_travel = travel
            tutor.available_for_online_teaching = online_teach
            tutor.help_with_homework  = homework
            tutor.full_time_teacher = full_time
            tutor.interested_in = interested_in
            tutor.save()
            ds={"name":tutor.name,"email":tutor.email}

            # Redirect to a success page or another view
            return render(request, 'personal_detail.html', {'email': email})  # Replace with actual page

    # If GET request, render the form template
    return render(request, 'teaching_detail_form.html', {'email': email})


def personal_detail(request,email):
    if request.method == "POST":
   
        profile_description = request.POST.get('profile_description')
        
        
        # Handle file uploads
        id_proof = request.FILES['id_proof']
        profile_photo = request.FILES['profile']
        number=request.POST.get("number")
        
        tutor = TutorRegistration.objects.filter(email=email).first()
        if tutor:
            otp = random.randint(100000, 999999)
            login={"otp":otp}
            html_template="otp.html"
            html_message=render_to_string(html_template,login)
        
            email_from=settings.EMAIL_HOST_USER
            r_list=[email]
            subject="Verification Otp"
            message=EmailMessage(subject,html_message,email_from,r_list)
            message.content_subtype='html'
            message.send()
            
            tutor.profile_description = profile_description
            tutor.id_proof=id_proof
            tutor.profile_photo=profile_photo
            tutor.phone=number
            tutor.filename=f'images/{profile_photo}'
            tutor.email_otp=otp
            print(tutor.filename)
            tutor.save()
            ds={"name":tutor.name,"email":tutor.email,"password":tutor.password,"number":tutor.phone,}
            




            return render(request,"otp_verfication_teachet.html",ds)
        return render(request,"personal_detail.html")
    return render(request,"personal_detail.html")

def otp_verify_teacher(request,email):
    if request.method=="POST":
        otp=request.POST.get("otp")
        print(type(otp),otp)
        t=TutorRegistration.objects.filter(email=email).first()
         
        if int(t.email_otp)==int(otp):
             return render( request,"teacher_dasboad.html",
                {
                    "all": TutorRegistration.objects.filter(email=t.email).values(),
                    "name": t.name,
                    "email": t.email,
                      "tutor":t
                },
            )
        else:
            return render(request, 'otp_verfication_teachet.html',{"name":t.name,"email":email,"msg":"Otp is incorrect"})
    
def teacher_email_verifed(request,email):
     tutor = TutorRegistration.objects.filter(email=email).first()
     ds={"name":tutor.name,"email":tutor.email}
     return render(request,"teacher_email_verifed.html",ds)

#teacher login
# def teach_login(request):
#     if request.method=="POST":
#         email=request.POST.get('email')
#         password=request.POST.get('password')

#         student = TutorRegistration.objects.filter(email=email,password=password).values
#         print(student)
#         if TutorRegistration.objects.filter(email=email,password=password).exists():
#             name=TutorRegistration.objects.filter(password=password).first()
#             return render(request,"teacher_dasboad.html",{"all":student,"name":name.name,"email":email})
#         else:
#             return render(request,"login.html",{"msg":"your login detail is Incorrect"})
   


#     return render(request,"login.html")

import re  # For email validation

def teach_login(request):
    if request.method == "POST":
        identifier = request.POST.get('email')  # Can be email or phone number
        password = request.POST.get('password')
        
        # Determine if the identifier is an email or a phone number
        if re.match(r'^\S+@\S+\.\S+$', identifier):  # Regex to validate email
            # Login with email
            teacher = TutorRegistration.objects.filter(email=identifier, password=password).first()
        else:
            # Login with phone number
            teacher = TutorRegistration.objects.filter(phone=identifier, password=password).first()
        user = authenticate(request, username=identifier , password=password)  # Authenticate using email
        
        if user is not None:
            login(request, user)
            request.session.set_expiry(60 * 60 * 24 * 7)  # 7 days
            if teacher:
                return redirect('teacher_dashboard')
            #     return render(
            #     request,
            #     "teacher_dasboad.html",
            #     {
            #         "all": TutorRegistration.objects.filter(email=teacher.email).values(),
            #         "name": teacher.name,
            #         "email": teacher.email,
            #     },
            # )
        else:
            return render(request, "login.html", {"msg": "Your login details are incorrect."})

    return render(request, "login.html")



@login_required
def teacher_dashboard(request):
    user = request.user  # Get the logged-in user

    # Fetch the tutor details
    tutors = TutorRegistration.objects.filter(email=user.email).first()

    if tutors:
        COIN_PACKS = [
       {"amount": 200, "label": "Starter Pack", "coins": 200, "bonus": 0, "total_coins": 200, "leads": 4, "effective_per_lead": 50},
       {"amount": 500, "label": "Basic Boost", "coins": 500, "bonus": 100, "total_coins": 600, "leads": 12, "effective_per_lead": 41.6},
       {"amount": 1000, "label": "Value Plus", "coins": 1000, "bonus": 250, "total_coins": 1250, "leads": 25, "effective_per_lead": 40},
       {"amount": 1500, "label": "Power User", "coins": 1500, "bonus": 400, "total_coins": 1900, "leads": 38, "effective_per_lead": 39.5},
       {"amount": 2000, "label": "Pro Pack", "coins": 2000, "bonus": 600, "total_coins": 2600, "leads": 52, "effective_per_lead": 38.5},
        {"amount": 3000, "label": "Ultimate Pack", "coins": 3000, "bonus": 900, "total_coins": 3900, "leads": 78, "effective_per_lead": 38.5},
        ]
        tutor_data = TutorRegistration.objects.filter(email=user.email).values()
        return render(request, "teacher_dasboad.html", {
            "all": tutor_data,
            "name": tutors.name,
            "email": tutors.email,
            "tutor":tutors,
            "coin_packs":COIN_PACKS
        })
    else:
        return render(request, "teacher_dasboad.html", {
            "msg": "Tutor details not found."
        })

def myprofile(request,email):
    tutor = TutorRegistration.objects.filter(email=email).values()
    first=TutorRegistration.objects.filter(email=email).first()
    p={"all":tutor,"name":first.name,"roll":first.job_roll,"first":first}
    
    return render(request,"h_myprofile.html",p)

def search_teacher(request,email):
    l=[
                       # Andhra Pradesh
    "Visakhapatnam, Andhra Pradesh", "Vijayawada, Andhra Pradesh", "Guntur, Andhra Pradesh", "Tirupati, Andhra Pradesh",
    "Kurnool, Andhra Pradesh", "Nellore, Andhra Pradesh", "Rajahmundry, Andhra Pradesh", "Kakinada, Andhra Pradesh",
    "Anantapur, Andhra Pradesh", "Kadapa, Andhra Pradesh", "Chittoor, Andhra Pradesh", "Eluru, Andhra Pradesh",
    "Machilipatnam, Andhra Pradesh", "Srikakulam, Andhra Pradesh", "Vizianagaram, Andhra Pradesh",

    # Arunachal Pradesh
    "Itanagar, Arunachal Pradesh", "Pasighat, Arunachal Pradesh", "Tawang, Arunachal Pradesh", "Ziro, Arunachal Pradesh",
    "Naharlagun, Arunachal Pradesh", "Bomdila, Arunachal Pradesh", "Tezu, Arunachal Pradesh", "Roing, Arunachal Pradesh",

    # Assam
    "Guwahati, Assam", "Dibrugarh, Assam", "Silchar, Assam", "Jorhat, Assam", 
    "Tinsukia, Assam", "Nagaon, Assam", "Tezpur, Assam", "Diphu, Assam",
    "Sibsagar, Assam", "Goalpara, Assam", "Barpeta, Assam", "Dhubri, Assam",

    # Bihar
    "Patna, Bihar", "Gaya, Bihar", "Bhagalpur, Bihar", "Muzaffarpur, Bihar",
    "Darbhanga, Bihar", "Purnia, Bihar", "Ara, Bihar", "Begusarai, Bihar",
    "Katihar, Bihar", "Munger, Bihar", "Chapra, Bihar", "Hajipur, Bihar",

    # Chhattisgarh
    "Raipur, Chhattisgarh", "Bilaspur, Chhattisgarh", "Durg, Chhattisgarh", "Korba, Chhattisgarh",
    "Raigarh, Chhattisgarh", "Jagdalpur, Chhattisgarh", "Ambikapur, Chhattisgarh", "Bhilai, Chhattisgarh",

    # Goa
    "Panaji, Goa", "Margao, Goa", "Vasco da Gama, Goa", "Mapusa, Goa",
    "Ponda, Goa", "Bicholim, Goa", "Canacona, Goa", "Curchorem, Goa",

    # Gujarat
    "Ahmedabad, Gujarat", "Surat, Gujarat", "Vadodara, Gujarat", "Rajkot, Gujarat",
    "Bhavnagar, Gujarat", "Jamnagar, Gujarat", "Junagadh, Gujarat", "Gandhinagar, Gujarat",
    "Nadiad, Gujarat", "Porbandar, Gujarat", "Vapi, Gujarat", "Morbi, Gujarat",

    # Haryana
    "Chandigarh, Haryana", "Gurugram, Haryana", "Faridabad, Haryana", "Hisar, Haryana",
    "Panipat, Haryana", "Ambala, Haryana", "Yamunanagar, Haryana", "Rohtak, Haryana",
    "Karnal, Haryana", "Panchkula, Haryana", "Sonipat, Haryana", "Kurukshetra, Haryana",

    # Himachal Pradesh
    "Shimla, Himachal Pradesh", "Dharamshala, Himachal Pradesh", "Mandi, Himachal Pradesh", "Kullu, Himachal Pradesh",
    "Manali, Himachal Pradesh", "Solan, Himachal Pradesh", "Una, Himachal Pradesh", "Bilaspur, Himachal Pradesh",

    # Jharkhand
    "Ranchi, Jharkhand", "Jamshedpur, Jharkhand", "Dhanbad, Jharkhand", "Bokaro, Jharkhand",
    "Deoghar, Jharkhand", "Hazaribagh, Jharkhand", "Giridih, Jharkhand", "Ramgarh, Jharkhand",

    # Karnataka
    "Bengaluru, Karnataka", "Mysuru, Karnataka", "Mangaluru, Karnataka", "Hubballi, Karnataka",
    "Belagavi, Karnataka", "Davangere, Karnataka", "Ballari, Karnataka", "Shivamogga, Karnataka",

    # Kerala
    "Thiruvananthapuram, Kerala", "Kochi, Kerala", "Kozhikode, Kerala", "Kollam, Kerala",

    # Madhya Pradesh
    "Bhopal, Madhya Pradesh", "Indore, Madhya Pradesh", "Gwalior, Madhya Pradesh", "Jabalpur, Madhya Pradesh",
    "Ujjain, Madhya Pradesh", "Sagar, Madhya Pradesh", "Rewa, Madhya Pradesh", "Satna, Madhya Pradesh",

    # Maharashtra
    "Mumbai, Maharashtra", "Pune, Maharashtra", "Nagpur, Maharashtra", "Nashik, Maharashtra",
    "Aurangabad, Maharashtra", "Thane, Maharashtra", "Kolhapur, Maharashtra", "Solapur, Maharashtra",

    # Manipur
    "Imphal, Manipur", "Thoubal, Manipur", "Kakching, Manipur", "Churachandpur, Manipur",

    # Meghalaya
    "Shillong, Meghalaya", "Tura, Meghalaya", "Nongpoh, Meghalaya", "Jowai, Meghalaya",

    # Mizoram
    "Aizawl, Mizoram", "Lunglei, Mizoram", "Champhai, Mizoram", "Serchhip, Mizoram",

    # Nagaland
    "Kohima, Nagaland", "Dimapur, Nagaland", "Mokokchung, Nagaland", "Tuensang, Nagaland",

    # Odisha
    "Bhubaneswar, Odisha", "Cuttack, Odisha", "Rourkela, Odisha", "Berhampur, Odisha",

    # Punjab
    "Amritsar, Punjab", "Ludhiana, Punjab", "Chandigarh, Punjab", "Jalandhar, Punjab",

    # Rajasthan
    "Jaipur, Rajasthan", "Jodhpur, Rajasthan", "Udaipur, Rajasthan", "Kota, Rajasthan",

    #Sikkim
    "Gangtok, Sikkim", "Namchi, Sikkim", "Mangan, Sikkim", "Pelling, Sikkim",

    # Tamil Nadu
    "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu",
    #Telangana
    "Hyderabad, Telangana", "Warangal, Telangana", "Nizamabad, Telangana", "Khammam, Telangana",

    # Tripura
    "Agartala, Tripura", "Dharmanagar, Tripura", "Kailashahar, Tripura", "Udaipur, Tripura",

    # Uttar Pradesh
    "Lucknow, Uttar Pradesh", "Kanpur, Uttar Pradesh", "Varanasi, Uttar Pradesh", "Agra, Uttar Pradesh",

    # Uttarakhand
    "Dehradun, Uttarakhand", "Haridwar, Uttarakhand", "Nainital, Uttarakhand", "Rishikesh, Uttarakhand",

    #West Bengal
    "Kolkata, West Bengal", "Asansol, West Bengal", "Durgapur, West Bengal", "Siliguri, West Bengal"
            ]
    account=Requestpost.objects.filter(email=email).first()
    accounts=TutorRequest.objects.filter(email=email).first()
    student = TutorRequest.objects.filter(email=email).first()
    if request.method=="POST":
        subject=request.POST.get('subject')
        location=request.POST.get('location')
       
        tutors = TutorRegistration.objects.all()

    # Filter based on subject and location
        if TutorRegistration.objects.filter(Q(subject__icontains=subject) & Q(location__icontains=location)).exists():

            tutors = TutorRegistration.objects.filter(Q(subject__icontains=subject)& Q(location__icontains=location)).values()
            

        elif TutorRegistration.objects.filter(Q(subject__icontains=subject)).exists():
            tutors=TutorRegistration.objects.filter(Q(subject__icontains=subject)).values()
            
        elif TutorRegistration.objects.filter(Q(location__icontains=location)).exists():
            tutors=TutorRegistration.objects.filter(Q(location__icontains=location)).values()
           
        else:
            tutors=TutorRegistration.objects.all()

        d={"tutors":tutors,"locations":l,"account":account,"accounts":accounts}
        return render(request, "all_teacher.html", d)
    all_tutor=TutorRegistration.objects.all()
    return render(request,"all_teacher.html",{"tutors":all_tutor,"locations":l,"account":student})





#_______________________________________________________________________________________________________________________________________
from urllib.parse import unquote
def fliter_location(request,location):
    l=[
                "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu"
            ]
    decoded_once = unquote(location)  # First level of decoding
    decoded_twice = unquote(decoded_once)   # Second level of decoding

    print(decoded_twice)
    if TutorRegistration.objects.filter(location=decoded_twice).exists():
        tutors=TutorRegistration.objects.filter(location=decoded_twice).values()
    else:
        tutors=TutorRegistration.objects.all().values()
    return render(request,"all_teacher.html",{"tutors":tutors,"locations":l,"heading":"All Tutors"})

#__________________________________________________________________________________
def online_tutor(request):
    l=[
                "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu"
            ]
    all_tutor=TutorRegistration.objects.filter(available_for_online_teaching="yes")
    return render(request,"all_teacher.html",{"tutors":all_tutor,"locations":l,"heading":"Online Tutors"})

def home_tutor(request):
    l=[
                "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu"
            ]
    all_tutor=TutorRegistration.objects.filter(willing_to_travel="yes")
    return render(request,"all_teacher.html",{"tutors":all_tutor,"locations":l,"heading":"Home Tutors"})

def search_teachers(request,email):
    l=[
                "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu"
            ]
    student=TutorRequest.objects.get(email=email)
    
    all_tutor=TutorRegistration.objects.all()
    account=Requestpost.objects.filter(email=email).first()
    accounts=TutorRequest.objects.filter(email=email).first()
    if request.method=="POST":
        
        subject=request.POST.get('subject')
        location=request.POST.get('location')
        if TutorRegistration.objects.filter(subject=subject,location=location).exists():
          
            tutors = TutorRegistration.objects.filter(subject=subject,location=location).values()
           
        elif TutorRegistration.objects.filter(subject=subject).exists():
            tutors=TutorRegistration.objects.filter(subject=subject).values()
        elif TutorRegistration.objects.filter(location=location).exists():
            tutors=TutorRegistration.objects.filter(location=location).values()
        d={"tutors":tutors,"locations":l,"account":account,"accounts":accounts}
        return render(request,"all_teacher.html",d)
   
    
    return render(request,"all_teacher.html",{"tutors":all_tutor,"locations":l,"name":student.name,"email":student.email,"account":account,"accounts":accounts})


def online_tutor(request,email):
    l=[
                "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu"
            ]
    all_tutor=TutorRegistration.objects.filter(available_for_online_teaching="yes")
    student=TutorRequest.objects.get(email=email)
    account=Requestpost.objects.filter(email=email).first()
    accounts=TutorRequest.objects.filter(email=email).first()
    return render(request,"online_tutors.html",{"tutors":all_tutor,"locations":l,"heading":"Online Tutors","name":student.name,"email":student.email,"account":account,"accounts":accounts})

def home_tutor(request,email):
    l=[
                "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu"
            ]
    student=TutorRequest.objects.get(email=email)
    all_tutor=TutorRegistration.objects.filter(willing_to_travel="yes")
    account=Requestpost.objects.filter(email=email).first()
    accounts=TutorRequest.objects.filter(email=email).first()
    return render(request,"home_tutor.html",{"tutors":all_tutor,"locations":l,"heading":"Online Tutors","name":student.name,"email":student.email,"account":account,"accounts":accounts})


def fliter_location(request,location,email):
    l=[
                "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu"
            ]
    decoded_once = unquote(location)  # First level of decoding
    decoded_twice = unquote(decoded_once)   # Second level of decoding
    student=TutorRequest.objects.get(email=email)
    account=Requestpost.objects.filter(email=email).first()
    accounts=TutorRequest.objects.filter(email=email).first()
    print(decoded_twice)
    if TutorRegistration.objects.filter(location=decoded_twice).exists():
        tutors=TutorRegistration.objects.filter(location=decoded_twice).values()
    else:
        tutors=TutorRegistration.objects.all().values()
    return render(request,"all_teacher.html",{"tutors":tutors,"locations":l,"heading":"All Tutors","name":student.name,"email":student.email,"account":account,"accounts":accounts})






def  student_inbox(request,email):
    account=Requestpost.objects.filter(email=email).first()
    accounts=TutorRequest.objects.filter(email=email).first()

    print("hee",accounts.email)
    if Message.objects.filter( receiver_email=email).exists():
        account=Requestpost.objects.filter(email=email).first()
        accounts=TutorRequest.objects.filter(email=email).first()
        sm=Message.objects.filter( receiver_email=email).values
     
        return render(request,"inbox.html",{"msg":sm,"account":account,"accounts":accounts})
    
    return render(request,"inbox.html",{"account":account,"accounts":accounts})

def student_post(request,email,id):
    if TutorRequest.objects.filter(email=email).exists():
        # objects=Requestpost.objects.all()
        # s=TutorRequest.objects.get(email=email)
        # sp=Requestpost.objects.get(id=id)/
          # Get all Requestpost objects
        objects = Requestpost.objects.all()

        # Retrieve specific TutorRequest and Requestpost instances
        s = get_object_or_404(TutorRequest, email=email)
        sp = get_object_or_404(Requestpost, id=id)
        for obj in objects:
            if obj.imagess and hasattr(obj.imagess, 'url'):
                obj.is_pdf = obj.imagess.url.endswith(".pdf")
            else:
                obj.is_pdf = False

        d = {"s": s, "sp": sp, "objects": objects}

        return render(request,"student_post.html",d)
    return render( request,"student_post.html")
    




#___________________student settings_____________________________

def stu_settings(request,email):
    account=Requestpost.objects.filter(email=email).first()
    accounts=TutorRequest.objects.filter(email=email).first()
    return render(request,"stu_settings.html",{"account":account,"accounts":accounts})


def student_profile(request,email):
    
    if request.method=="POST":
         student=Requestpost.objects.filter(email=email).first()
         profile_photo = request.FILES['profile']
         if student:
            student.profile_photo=profile_photo

            student.filename=f'stu_images/{profile_photo}'
            student.save()
            
            
            
            return render(request,"stu_settings.html",{"msg":" your Profile Photo added","accounts":student})
         else:  
             return render(request,"stu_settings.html",{"msg":"your Profile Photo not added"})
    return render(request,"stu_settins.html")


def change_e(request,email):
    if request.method=="POST":
        emails=request.POST.get('email')

        Requestpost.objects.filter(email=email).update(email=emails)
        TutorRequest.objects.filter(email=email).update(email=emails)
        account=Requestpost.objects.filter(email=emails).first()
        accounts=TutorRequest.objects.filter(email=emails).first()
        return render(request,"stu_settings.html",{"msg":" update your mail","account":account,"accounts":accounts})
def change_ph(request, email):
    if request.method == "POST":
        phone = request.POST.get('phone')

        TutorRequest.objects.filter(email=email).update(phone=phone)
        account = Requestpost.objects.filter(email=email).first()
        accounts = TutorRequest.objects.filter(email=email).first()
        messages.success(request, "Phone Number is updated")
        
        return redirect("myposts")  # ✅ Return the redirect

    return redirect("myposts") 


#basci detail edit
def t_basic(request,email):
    a=TutorRegistration.objects.filter(email=email).first()
    if request.method=="POST":
      
        strength = request.POST.get('strength')
        gender = request.POST.get('gender')
        location = request.POST.get('location')
        language = request.POST.get('lanquage')
        if strength:
            TutorRegistration.objects.filter(email=email).update(strength=strength)
        if gender:
            TutorRegistration.objects.filter(email=email).update(gender=gender)
        if location:
            TutorRegistration.objects.filter(email=email).update(location=location)
        if language:
            TutorRegistration.objects.filter(email=email).update(language=language)
        return render(request,"t_basic_detail.html",{"account":a,"msg":"succfully updated your deatils"})
    return render(request,"t_basic_detail.html",{"account":a})

def t_photo(request,email):
    a=TutorRegistration.objects.filter(email=email).first()
    if request.method=="POST":
        profile_photo = request.FILES['profile']
        filename=f'images/{profile_photo}'
        a.profile_photo=profile_photo
        TutorRegistration.objects.filter(email=email).update(filename=filename)
        a=TutorRegistration.objects.filter(email=email).first()
        messages.success(request, f"photos are updated")
        return redirect('teacher_dashboard')

    return render(request,"t_photo_change.html",{"account":a})

def t_subject(request,email):
    a=TutorRegistration.objects.filter(email=email).first()
    if request.method=="POST":
        subject = request.POST.get('subject')
        level = request.POST.get('level')
        to_level = request.POST.get('to_level')
            #two
        two_subject = request.POST.get('two_subject')
        two_level = request.POST.get('two_level')
        two_to_level = request.POST.get('to_level')
            #three
        three_subject = request.POST.get('three_subject')
        three_level = request.POST.get('three_level')
        three_to_level = request.POST.get('three_to_level')
            #four
        four_subject = request.POST.get('four_subject')
        four_level = request.POST.get('four_level')
        four_to_level = request.POST.get('four_to_level')

            #five
        five_subject = request.POST.get('five_subject')
        five_level = request.POST.get('five_level')
        five_to_level = request.POST.get('five_to_level')
       
            # Update the tutor details from the POST data
        if subject:
            TutorRegistration.objects.filter(email=email).update(subject=subject)
            TutorRegistration.objects.filter(email=email).update(from_level=level)
            TutorRegistration.objects.filter(email=email).update(to_level=to_level)
            return render(request,"t_subject.html",{"account":a,"msg":"updated ! subject of one"})
        if two_subject:
            TutorRegistration.objects.filter(email=email).update(two_subject=two_subject)
            TutorRegistration.objects.filter(email=email).update(two_from_level=two_level)
            TutorRegistration.objects.filter(email=email).update(two_to_level=two_to_level)
            return render(request,"t_subject.html",{"account":a,"msg":"updated ! subject of two"})
        if three_subject:
            TutorRegistration.objects.filter(email=email).update(three_subject=three_subject)
            TutorRegistration.objects.filter(email=email).update(three_from_level=three_level)
            TutorRegistration.objects.filter(email=email).update(three_to_level=three_to_level)
            return render(request,"t_subject.html",{"account":a,"msg":"updated ! subject of three"})
        if four_subject:
           TutorRegistration.objects.filter(email=email).update(four_subject=four_subject)
           TutorRegistration.objects.filter(email=email).update(four_from_level=four_level)
           TutorRegistration.objects.filter(email=email).update(four_to_level=four_to_level)
           return render(request,"t_subject.html",{"account":a,"msg":"updated ! subject of four"})


        if five_subject:
            TutorRegistration.objects.filter(email=email).update(five_subject=five_subject)
            TutorRegistration.objects.filter(email=email).update(five_from_level=five_level)
            TutorRegistration.objects.filter(email=email).update(five_to_level=five_to_level)
            return render(request,"t_subject.html",{"account":a,"msg":"updated ! subject of five"})

        

            
            
           

            # Save the updated details
           
        return render(request,"t_subject.html",{"account":a,"msg":"updated ! your photo"})

    return render(request,"t_subject.html",{"account":a})

def change_p(request,email):
    a = TutorRegistration.objects.filter(email=email).first()
    login={"name":a.name,"email":a.email,"password":a.password}
    html_template="email_c_p.html"
    html_message=render_to_string(html_template,login)
    email_from=settings.EMAIL_HOST_USER
    r_list=[email]
    subject="Action required: your old password form  Learnersleaf"
    message=EmailMessage(subject,html_message,email_from,r_list)
    message.content_subtype='html'
    message.send()
    return render(request,"t_contact.html",{"account":a})

from django.contrib.auth.hashers import make_password, check_password

def t_contact(request, email):
    a = TutorRegistration.objects.filter(email=email).first()
    
    if request.method == "POST":
        new_email = request.POST.get('email')
        phone = request.POST.get('phone')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        
        # Update email
        if new_email and new_email != a.email:
            TutorRegistration.objects.filter(email=email).update(email=new_email)
            a = TutorRegistration.objects.filter(email=new_email).first()  # Re-fetch the updated instance
            return render(request, "t_contact.html", {"account": a, "msg": "Updated your email!"})
        
        # Update phone number
        if phone and phone != a.phone:
            TutorRegistration.objects.filter(email=email).update(phone=phone)
            return render(request, "t_contact.html", {"account": a, "msg": "Updated your phone number!"})
        
        # Update password
        if old_password and new_password:
            # Verify the old password
            if old_password== a.password:  # Ensure you use hashed passwords
                print("hello")
                TutorRegistration.objects.filter(email=email).update(password=new_password)
                print("hello")
                return render(request, "t_contact.html", {"account": a, "msg": "Updated your password!"})
            else:
                return render(request, "t_contact.html", {"account": a, "msg": "Old password is incorrect."})
    
    return render(request, "t_contact.html", {"account": a})

def t_teaching(request,email):
    a = TutorRegistration.objects.filter(email=email).first()
    if request.method == "POST":
        i_charge = request.POST.get('i_charge')
        min_fee = request.POST.get('min_fee')
        max_fee = request.POST.get('max_fee')
        total_experience = request.POST.get('total_experience')
        teaching_experience = request.POST.get('teaching_experience')
        online_experience = request.POST.get('online_experience')
        travel = request.POST.get('travel')
        online_teach = request.POST.get('online_teach')
        homework = request.POST.get('homework')
        full_time = request.POST.get('full_time')
        interested_in = request.POST.get('interested_in')

        # Fetch the tutor record based on the email
        tutor = TutorRegistration.objects.filter(email=email).first()

        if tutor:
            # Update the tutor's details with the form data
            
            tutor.i_charge = i_charge
            tutor.min_fee = min_fee
            tutor.max_fee = max_fee
            tutor.total_experience = total_experience
            tutor.teaching_experience = teaching_experience
            tutor.online_experience = online_experience
            tutor.willing_to_travel = travel
            tutor.available_for_online_teaching = online_teach
            tutor.help_with_homework  = homework
            tutor.full_time_teacher = full_time
            tutor.interested_in = interested_in
            tutor.save()
            a = TutorRegistration.objects.filter(email=email).first()
            return render(request, "t_teaching.html", {"account": a, "msg": "update you teaching details."})

    return render(request, "t_teaching.html", {"account": a})

def t_experience(request,email):
    a = TutorRegistration.objects.filter(email=email).first()
    if request.method=="POST":
          company_name=request.POST.get('company_name')
          job_roll=request.POST.get('job_roll')
          start_date=request.POST.get('start_date')
          end_date=request.POST.get('end_date')
          job_description=request.POST.get('job_description')

          tutor = TutorRegistration.objects.filter(email=email).first()
          tutor.company_name=company_name
          tutor.job_roll=job_roll
          tutor.job_start_date=start_date
          if end_date:
              tutor.job_end_date=end_date
          tutor.save()
          a = TutorRegistration.objects.filter(email=email).first()
          return render(request, "t_experience.html", {"account": a, "msg": "update you teaching details."})
    return render(request, "t_experience.html", {"account": a})
from django.db.models import Q  

# job search
def search_job(request):
  
    if request.method=="POST":
        subject=request.POST.get('subject')
        location=request.POST.get('location')
        if Requestpost.objects.filter( Q(subject=subject) | Q(two_subject=subject) | Q(three_subject=subject) | Q(four_subject=subject) | Q(five_subject=subject),location=location).exists():
          
            tutors = Requestpost.objects.filter( Q(subject=subject) | Q(two_subject=subject) | Q(three_subject=subject) | Q(four_subject=subject) | Q(five_subject=subject),location=location).values()
            d={"all":tutors}
           
        elif Requestpost.objects.filter( Q(subject=subject) | Q(two_subject=subject) | Q(three_subject=subject) | Q(four_subject=subject) | Q(five_subject=subject)).exists():
            tutors=Requestpost.objects.filter( Q(subject=subject) | Q(two_subject=subject) | Q(three_subject=subject) | Q(four_subject=subject) | Q(five_subject=subject)).values()
            d={"all":tutors}
        elif Requestpost.objects.filter(Q(location__icontains=location)).exists():
            tutors=Requestpost.objects.filter(Q(location__icontains=location)).values()
            d={"all":tutors}

        
        else:
            
            d={"t":"All Job","msg":"There is no Data Found"}
        
      
        d={"all":tutors}
        return render(request,"tutors_job.html",d)
    all_tutor=TutorRegistration.objects.all()
    return render(request,"tutors_job.html",{"all":all_tutor})

def search_jobs(request,email):
  
    if request.method=="POST":
        a = TutorRegistration.objects.filter(email=email).first()

        all=Requestpost.objects.all()
        subject=request.POST.get('subject')
        location=request.POST.get('location')
        if Requestpost.objects.filter( Q(subject=subject) | Q(two_subject=subject) | Q(three_subject=subject) | Q(four_subject=subject) | Q(five_subject=subject),location=location).exists():
          
            tutors = Requestpost.objects.filter( Q(subject=subject) | Q(two_subject=subject) | Q(three_subject=subject) | Q(four_subject=subject) | Q(five_subject=subject),location=location).values()
            d={"all":tutors,"account":a,"t":"All Job"}
           
        elif Requestpost.objects.filter( Q(subject=subject) | Q(two_subject=subject) | Q(three_subject=subject) | Q(four_subject=subject) | Q(five_subject=subject)).exists():
            tutors=Requestpost.objects.filter( Q(subject=subject) | Q(two_subject=subject) | Q(three_subject=subject) | Q(four_subject=subject) | Q(five_subject=subject)).values()
            d={"all":tutors,"account":a,"t":"All Job"}
        elif Requestpost.objects.filter(Q(location__icontains=location)).exists():
            tutors=Requestpost.objects.filter(Q(location__icontains=location)).values()
            d={"all":tutors,"account":a,"t":"All Job"}

        else:
            
            d={"account":a,"t":"All Job","msg":"There is no Data Found"}

       
       
        return render(request,"tutors_job.html",d)
    all_tutor=TutorRegistration.objects.all()
    return render(request,"tutors_job.html",{"all":all_tutor})

def tutors_job(request,email):

    a = TutorRegistration.objects.filter(email=email).first()
    all=Requestpost.objects.all()
    return render(request,"tutors_job.html",{"all":all,"account":a,"t":"All Job"})
def tutors_online_job(request,email):
    a = TutorRegistration.objects.filter(email=email).first()
    all=Requestpost.objects.all()
    return render(request,"tutors_job.html",{"all":all,"account":a,"t":"Online Job"})




def h_fliter_location(request,location):
  
    return render(request,"h_all_teacher.html")

#job---

from django.db.models import Q

def search_jobs(request):
    if request.method == "POST":
        subject = request.POST.get('subject', '').strip()
        location = request.POST.get('location', '').strip()

        # Base query
        query = Q()
        if subject:
            query &= (
                Q(subject__icontains=subject) |
                Q(two_subject__icontains=subject) |
                Q(three_subject__icontains=subject) |
                Q(four_subject__icontains=subject) |
                Q(five_subject__icontains=subject)
            )
        if location:
            query &= Q(location__icontains=location)

        tutors = Requestpost.objects.filter(query).values()

        if tutors:
             if request.user.is_authenticated:
                if TutorRegistration.objects.filter(email=request.user.email).exists():
                    a = TutorRegistration.objects.filter(email=request.user.email).first()
                    all=Requestpost.objects.all()
                    return render(request,"tutors_job.html",{"all":tutors,"account":a,"h":"all"})
                else:
                    all=Requestpost.objects.all()
                    return render(request,"tutors_job.html",{"t":"You are not a tutor","all":all,"h":"all"})
             else:
                all=Requestpost.objects.all()
                return render(request,"tutors_job.html",{"all":tutors,"h":"all"})
            
        else:
            if request.user.is_authenticated:
                if TutorRegistration.objects.filter(email=request.user.email).exists():
                    a = TutorRegistration.objects.filter(email=request.user.email).first()
                    all=Requestpost.objects.all()
                    return render(request,"tutors_job.html",{"t": "There is no Data Found","account":a,"h":"all"})
                else:
                    all=Requestpost.objects.all()
                    return render(request,"tutors_job.html",{"t":"You are not a tutor","all":all,"h":"all"})
            else:
                all=Requestpost.objects.all()
                return render(request,"tutors_job.html",{"t":"You are not a tutor","h":"all"})
            

    # For GET requests or other cases
    return render(request, "tutors_job.html")

 

def h_tutors_job(request):
    if request.user.is_authenticated:
        if TutorRegistration.objects.filter(email=request.user.email).exists():
            a = TutorRegistration.objects.filter(email=request.user.email).first()
            all=Requestpost.objects.all()
            return render(request,"tutors_job.html",{"all":all,"account":a,"h":"all"})
        else:
            all=Requestpost.objects.all()
            return render(request,"tutors_job.html",{"t":"You are not a tutor","all":all,"h":"all"})
    else:
        all=Requestpost.objects.all()
        return render(request,"tutors_job.html",{"all":all,"h":"all"})

def h_online_job(request):
    if request.user.is_authenticated:
        if TutorRegistration.objects.filter(email=request.user.email).exists():
            a = TutorRegistration.objects.filter(email=request.user.email).first()
            all=Requestpost.objects.filter(meeting_option="Online").values
            return render(request,"tutors_job.html",{"all":all,"account":a,"h":"online"})
        else:
            all=Requestpost.objects.filter(meeting_option="Online").values
            return render(request,"tutors_job.html",{"t":"You are not a tutor","all":all,"h":"online"})
    else:
        all=Requestpost.objects.all()
        return render(request,"tutors_job.html",{"all":all,"h":"online"})
    

def h_home_job(request):
    if request.user.is_authenticated:
        if TutorRegistration.objects.filter(email=request.user.email).exists():
            a = TutorRegistration.objects.filter(email=request.user.email).first()
            all=Requestpost.objects.filter(meeting_option="Offline").values
            return render(request,"tutors_job.html",{"all":all,"account":a,"h":"home"})
        else:
            all=Requestpost.objects.all()
            return render(request,"tutors_job.html",{"t":"You are not a tutor","all":all,"h":"home"})
    else:
        all=Requestpost.objects.filter(meeting_option="Offline").values
        return render(request,"tutors_job.html",{"all":all,"h":"home"})



# tutors
def h_all_teachers(request ):
    
    all_tutor=TutorRegistration.objects.all()
    print("all :",all_tutor)
    for i in all_tutor:
        print(i.available_for_online_teaching)
        print(i.willing_to_travel)
    return render(request,"h_all_teacher.html",{"tutors":all_tutor,"h":"all"})




from django.db.models import Q

def h_search_teacher(request):
    if request.method == "POST":
        subject_input = request.POST.get('subject', '').strip().lower()
        location_input = request.POST.get('location', '').strip().lower()

        print("User input - subject:", subject_input)
        print("User input - location:", location_input)

        query = Q()

        if subject_input:
            query &= Q(subject__icontains=subject_input)

        if location_input:
            query &= Q(location__icontains=location_input)

        tutors = TutorRegistration.objects.filter(query)

        print("Found tutors:", tutors)

        if tutors:
            return render(request, "h_all_teacher.html", {"tutors": tutors})
        else:
            return render(request, "h_all_teacher.html", {"t": "There is no Data Found"})

    return render(request, "h_all_teacher.html")



def h_online_tutor(request):
    
    all_tutor=TutorRegistration.objects.filter(available_for_online_teaching="Yes")
    print("online",all_tutor)
    return render(request,"h_all_teacher.html",{"tutors":all_tutor,"h":"online"})

def h_home_tutor(request):
   
   
    all_tutor=TutorRegistration.objects.filter(willing_to_travel="Yes")
    print("home",all_tutor)
    return render(request,"h_all_teacher.html",{"tutors":all_tutor,"h":"home"})





def  buy_coin_stu(request,email,coins):
    c=TutorRequest.objects.filter(email=email).first()
    print(c.coin)
    if c.coin:
        c.coin=c.coin+coins
        c.save()
    else:
        c.coin=coins
        c.save()
    messages.success(request, f"coin are updated")
    return redirect("myposts")
   
def  s_wallet(request,email):
    c=TutorRequest.objects.filter(email=email).first()
    COIN_PACKS = [
    {"amount": 200, "label": "Basic"},
    {"amount": 500, "label": "Starter"},
    {"amount": 1000, "label": "Pro"},
    {"amount": 1500, "label": "Premium"},
    {"amount": 3000, "label": "Ultimate"},
]
    return render(request,"s_wallet.html",{"account":c,"coin_packs":COIN_PACKS})

def  buy_coin_stus(request,amount):
    user = request.user if request.user.is_authenticated else None
    amount =amount
    coins=amount
    if amount==200:
        coins = amount
    elif amount==500:
        coins=600
    elif amount==1000:
        coins=1250
    elif amount==1500:
        coins=1900
    elif amount==2000:
        coins=2600
    order_id = str(uuid.uuid4())  # Unique order I
    transaction = Transaction.objects.create(
            user=user.email,
            amount=amount,
            coins=coins,
            order_id=order_id,
        )

        # Prepare headers for Cashfree
    headers = {
            "Content-Type": "application/json",
            "x-api-version": "2022-01-01",
            "x-client-id": settings.CASHFREE_APP_ID,
            "x-client-secret": settings.CASHFREE_SECRET_KEY
        }

        # Create order data
    data = {
            "order_id": order_id,
            "order_amount": amount,
            "order_currency": "INR",
            "customer_details": {
                "customer_id": str(user.id) if user else str(uuid.uuid4()),
                "customer_email": user.email if user else "guest@example.com",
                "customer_phone": "+919090407368"
            },
            "order_meta": {
                "return_url": f"https://learnersleaf.com//payment/verify/?order_id={order_id}"
            }
        }

    response = requests.post(f"{settings.CASHFREE_BASE_URL}/orders", json=data, headers=headers)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
    if response.status_code == 200:
            payment_data = response.json()
            return redirect(payment_data['payment_link'])
    else:
            return render(request, 'payment_failed.html', {"message": "Payment gateway error."})

    # Show buy_coins.html with current balance and coin packs

def verify_payment(request):
    order_id = request.GET.get("order_id")

    headers = {
        "Content-Type": "application/json",
        "x-api-version": "2022-01-01",
        "x-client-id": settings.CASHFREE_APP_ID,
        "x-client-secret": settings.CASHFREE_SECRET_KEY
    }

    # Check the payment status from Cashfree API
    res = requests.get(f"{settings.CASHFREE_BASE_URL}/orders/{order_id}", headers=headers)
    data = res.json()

    try:
        transaction = Transaction.objects.get(order_id=order_id)
    except Transaction.DoesNotExist:
        return render(request, "payment_failed.html", {"message": "Transaction not found."})

    # Prevent re-adding coins on refresh
    if transaction.status == "SUCCESS":
        wallet, created = TutorRequest.objects.get_or_create(email=transaction.user)
        return render(request, "payment_success.html", {
        "coins": transaction.coins,
        "balance": wallet.coin
    })

    # If payment was successful
    if data.get("order_status") == "PAID":
        transaction.status = "SUCCESS"
        transaction.payment_id = data.get("order_token", "")
        transaction.save()

        wallet, created = TutorRequest.objects.get_or_create(email=transaction.user)
        print("t",transaction.coins)
        wallet.coin =(wallet.coin or 0)+ transaction.coins
        wallet.save()
        print("wallet",wallet.coin)

        return render(request, "payment_success.html", {
            "coins": transaction.coins,
            "balance": wallet.coin
        })

    # Otherwise, mark as failed
    transaction.status = "FAILED"
    transaction.save()
    return render(request, "payment_failed.html", {
        "message": "Payment was not successful."
    })



def  buy_coin_teacher(request,amount):
    user = request.user if request.user.is_authenticated else None
    amount =amount
    coins=amount
    if amount==200:
        coins = amount
    elif amount==500:
        coins=600
    elif amount==1000:
        coins=1250
    elif amount==1500:
        coins=1900
    elif amount==2000:
        coins=2600
    order_id = str(uuid.uuid4())  # Unique order I
    transaction = Transaction.objects.create(
            user=user.email,
            amount=amount,
            coins=coins,
            order_id=order_id,
        )

        # Prepare headers for Cashfree
    headers = {
            "Content-Type": "application/json",
            "x-api-version": "2022-01-01",
            "x-client-id": settings.CASHFREE_APP_ID,
            "x-client-secret": settings.CASHFREE_SECRET_KEY
        }

        # Create order data
    data = {
            "order_id": order_id,
            "order_amount": amount,
            "order_currency": "INR",
            "customer_details": {
                "customer_id": str(user.id) if user else str(uuid.uuid4()),
                "customer_email": user.email if user else "guest@example.com",
                "customer_phone": "+919090407368"
            },
            "order_meta": {
                "return_url": f"https://learnersleaf.com/payment/verify_teacher/?order_id={order_id}"
            }
        }

    response = requests.post(f"{settings.CASHFREE_BASE_URL}/orders", json=data, headers=headers)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
    if response.status_code == 200:
            payment_data = response.json()
            return redirect(payment_data['payment_link'])
    else:
            return render(request, 'payment_failed_teacher.html', {"message": "Payment gateway error."})

    # Show buy_coins.html with current balance and coin packs

def verify_payment_teacher(request):
    order_id = request.GET.get("order_id")

    headers = {
        "Content-Type": "application/json",
        "x-api-version": "2022-01-01",
        "x-client-id": settings.CASHFREE_APP_ID,
        "x-client-secret": settings.CASHFREE_SECRET_KEY
    }

    # Check the payment status from Cashfree API
    res = requests.get(f"{settings.CASHFREE_BASE_URL}/orders/{order_id}", headers=headers)
    data = res.json()

    try:
        transaction = Transaction.objects.get(order_id=order_id)
    except Transaction.DoesNotExist:
        return render(request, "payment_failed_teacher.html", {"message": "Transaction not found."})

    # Prevent re-adding coins on refresh
    if transaction.status == "SUCCESS":
        wallet, created = TutorRegistration.objects.get_or_create(email=transaction.user)
        return render(request, "payment_success_teacher.html", {
        "coins": transaction.coins,
        "balance": wallet.coin
    })

    # If payment was successful
    if data.get("order_status") == "PAID":
        transaction.status = "SUCCESS"
        transaction.payment_id = data.get("order_token", "")
        transaction.save()

        wallet, created = TutorRegistration.objects.get_or_create(email=transaction.user)
        print("t",transaction.coins)
        wallet.coin =(wallet.coin or 0)+ transaction.coins
        wallet.save()
        print("wallet",wallet.coin)

        return render(request, "payment_success_teacher.html", {
            "coins": transaction.coins,
            "balance": wallet.coin
        })

    # Otherwise, mark as failed
    transaction.status = "FAILED"
    transaction.save()
    return render(request, "payment_failed_teacher.html", {
        "message": "Payment was not successful."
    })





def  t_wallet(request,email):
    c=TutorRegistration.objects.filter(email=email).first()

    return render(request,"t_wallet.html",{"account":c})
def  buy_coin_teach(request,email,coins):
    print(coins)
   
    c=TutorRegistration.objects.filter(email=email).first()
    if c.coin:
        c.coin=c.coin+coins
        c.save()
    else:
        c.coin=coins
        c.save()

    messages.success(request, f" coins are added")
    return redirect("teacher_dashboard")


def view_post_teach(request,a_email,email,id):
    print(email)
    if TutorRegistration.objects.filter(email=a_email).exists():
        if teacher_addcard.objects.filter(email=a_email,cid=id).exists():
            s=TutorRequest.objects.filter(email=email).first()
            sp=Requestpost.objects.get(id=id)
            c=TutorRegistration.objects.filter(email=a_email).first()
            d={"s":s,"sp":sp,"account":c}
            return render(request,"v_full_student_post.html",d)
        else:
            s=TutorRequest.objects.filter(email=email).first()
            sp=Requestpost.objects.get(id=id)
            c=TutorRegistration.objects.filter(email=a_email).first()
            d={"s":s,"sp":sp,"account":c}
       
            return render(request,"v_student_post.html",d)
    messages.success(request, f"Leaner cannot view Another Leaner Profile")
    return redirect("h_tutors_job")
def use_coin_teach(request,a_email,email,id):
    c=TutorRegistration.objects.filter(email=a_email).first()
    
    print(c.coin)
    if c.coin:
        print(c.coin)
        if c.coin>=100:
            c.coin=c.coin-50
            c.save()
            sp=Requestpost.objects.get(id=id)
            cp=sp.count
            cp=cp+1
            
            
            print(cp)
            Requestpost.objects.filter(id=id).update(count=cp)
            teacher_addcard.objects.create(email=a_email,cid=id)
            s=TutorRequest.objects.filter(email=email).first()
            
            c=TutorRegistration.objects.filter(email=a_email).first()
            d={"s":s,"sp":sp,"account":c}
            return render(request,"v_full_student_post.html",d)
        else:
            c=TutorRegistration.objects.filter(email=a_email).first()
            messages.success(request, f"your as Insufficient Balance coin  so! buy coin")
            return redirect("teacher_dashboard")
            
    else:
      c=TutorRegistration.objects.filter(email=a_email).first()
      messages.success(request, f"your as Insufficient Balance coin  so! buy coin")
      return redirect("teacher_dashboard")
    
def t_message_to(request,s_email,r_email):
    teacher=TutorRegistration.objects.filter(email=s_email).first()
    if request.method=="POST":
        subject=request.POST.get('subject')
        message =request.POST.get('message')
        receiver_email=r_email
        sender_email=s_email
        Message.objects.create(sender_name=teacher.name,sender_email=sender_email,receiver_email=receiver_email,subject=subject,body=message)

        return render(request,"message.html",{"msg":"message is sented","name":teacher.name,"account":teacher})


        
    
    return render(request,"message.html",{"name":teacher.name,"s_email":s_email,"r_email":r_email, "account":teacher})   

def  teacher_inbox(request,email):
    c=TutorRegistration.objects.filter(email=email).first()
    if Message.objects.filter( receiver_email=email).exists():
        sm=Message.objects.filter( receiver_email=email).values

     
        return render(request,"t_inbox.html",{"msg":sm,"account":c})
    
    return render(request,"t_inbox.html",{"account":c})

def student_update(request,email,id):
    post = Requestpost.objects.get(id=id)
    student = TutorRequest.objects.filter(email=email).first()
    if request.method=="POST":
        classes=request.POST.get("classes")
        cariculam=request.POST.get("curriculum")
        dyr = request.POST.get("dyr")
       
        subject = request.POST.get("subject")
        two_subject = request.POST.get("two_subject")
        three_subject = request.POST.get("three_subject")
        four_subject=request.POST.get("four_subject")
        five_subject=request.POST.get("five_subject")
        i_want = request.POST.get("i_want")
        meeting_option= request.POST.get("meeting_option")
        budget = request.POST.get("budget")
        budget_need = request.POST.get("budget_need")
        
        language = request.POST.get("language")
       
        need = request.POST.get("need")
        
        gender = request.POST.get("gender")
        l=TutorRequest.objects.filter(email=email).first()
        r=Requestpost.objects.filter(id=id).update(
            
            email=email,
            curriculum=cariculam,
            classes=classes,
            dyr=dyr,
            
            subject=subject,
            two_subject=two_subject,
            three_subject=three_subject,
            four_subject=four_subject,
            five_subject=five_subject,
            i_want=i_want,
            meeting_option=meeting_option,
         
            budget=budget,
            budget_need=budget_need,
            gender=gender,
            language=language,
           
            need=need,
           
            location=l.location
            )
 
        post = Requestpost.objects.filter(email=email).values
        student = TutorRequest.objects.filter(email=email).first()
        messages.success(request, f"Welcome !! {student.name}")  # Add success message
        return redirect("myposts")
    return render(request,"stu_edit.html",{"all":post,"post":student})


def s_myprofile(request,email,s_email):
    if TutorRequest.objects.filter(email=s_email).exists():
    
        tutor = TutorRegistration.objects.filter(email=email).values()
        first=TutorRegistration.objects.filter(email=email).first()
        p={"all":tutor,"name":first.name,"roll":first.job_roll,"first":first,"s_email":s_email}
        return render(request,"myprofile.html",p)
    messages.success(request, f"Tutor cannot view Another Tutor Profile")
    return redirect('h_all_teachers')
def view_message_stu(request,a_email,email,id):
    print(email)
    c=TutorRequest.objects.filter(email=a_email).first()
    if  student_addcard.objects.filter(email=a_email,cid=id).exists():
       return redirect('t_message_to', s_email=a_email, r_email=email)
  
    elif c.coin:
        print(c.coin)
        if c.coin>=100:
            c.coin=c.coin-100
            c.save()
            student_addcard.objects.create(email=a_email,cid=id)
            return redirect('t_message_to', s_email=a_email, r_email=email)

    else:
        c=TutorRequest.objects.filter(email=a_email).first()
        return render(request,"s_wallet.html",{"account":c})
def view_contant_stu(request,a_email,email,id):
    print(email)
    c=TutorRequest.objects.filter(email=a_email).first()
    tutor = TutorRegistration.objects.filter(email=email).values()
    first=TutorRegistration.objects.filter(email=email).first()
    if  student_addcard.objects.filter(email=a_email,cid=id).exists():
        tutor = TutorRegistration.objects.filter(email=email).values()
        first=TutorRegistration.objects.filter(email=email).first()
        p={"all":tutor,"name":first.name,"roll":first.job_roll,"first":first,"s_email":a_email,"phone":first.phone,"email":first.email}
        return render(request,"myprofile.html",p)
    else:
        p={"all":tutor,"name":first.name,"roll":first.job_roll,"first":first,"s_email":a_email,"phone":first.phone,"option":"option"}
        return render(request,"myprofile.html",p)

  

def use_coin_view_contant_stu(request,a_email,email,id):
    c=TutorRequest.objects.filter(email=a_email).first()
    if c.coin:
        print(c.coin)
        if c.coin>=100:
            c.coin=c.coin-50
            c.save()
            student_addcard.objects.create(email=a_email,cid=id)
            tutor = TutorRegistration.objects.filter(email=email).values()
            first=TutorRegistration.objects.filter(email=email).first()
            p={"all":tutor,"name":first.name,"roll":first.job_roll,"first":first,"s_email":a_email,"phone":first.phone,"email":first.email}
            return render(request,"myprofile.html",p)
    else:
        c=TutorRequest.objects.filter(email=a_email).first()
        messages.success(request, f"You have insufficient balance in your wallet to buy coins.")
        return redirect("myposts")


def t_forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if TutorRegistration.objects.filter(email=email).exists():
            tutor=TutorRegistration.objects.filter(email=email).first()
            login={"name":tutor.name,"email":email,"password":tutor.password}
            html_template="a_email_verify.html"
            html_message=render_to_string(html_template,login)
        
            email_from=settings.EMAIL_HOST_USER
            r_list=[email]
            subject="Action required: Please confirm to post requirement"
            message=EmailMessage(subject,html_message,email_from,r_list)
            message.content_subtype='html'
            message.send()
            return render(request,"t_forget.html",{"msg":"Check your mail and change your password"})
        else:
            return render(request,"t_forget.html",{"msg":"Email not found"})
    return render(request,"t_forget.html")

def change_password(request,email):
    if request.method=="POST":
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password==confirm_password:
            TutorRegistration.objects.filter(email=email).update(password=password)
            return render(request,"login.html",{"msg":"your password is changed!!!!! Start login"})
        else:
            return render(request,"t_change_p.html",{"msg":"password and confirm password not match"})
        


    return render(request,"t_change_p.html",{"email":email})

    



def home(request):
    return render(request,"new_home.html")

def about(request):
    return render(request,"about.html")


def delete_all(request):
   TutorRequest.objects.all().delete()
   TutorRegistration.objects.all().delete()
   Message.objects.all().delete()   
   teacher_addcard.objects.all().delete()
   student_addcard.objects.all().delete()
   Requestpost.objects.all().delete()
   return render(request,"home.html")

def delete_stu(request):
    TutorRequest.objects.all().delete()
    student_addcard.objects.all().delete()
    return render(request,"home.html")


def s_forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if TutorRequest.objects.filter(email=email).exists():
            tutor=TutorRequest.objects.filter(email=email).first()
            login={"name":tutor.name,"email":email,"password":tutor.password}
            html_template="s_mail_verify.html"
            html_message=render_to_string(html_template,login)
        
            email_from=settings.EMAIL_HOST_USER
            r_list=[email]
            subject="Action required: Please confirm to post requirement"
            message=EmailMessage(subject,html_message,email_from,r_list)
            message.content_subtype='html'
            message.send()
            return render(request,"s_forget.html",{"msg":"Check your mail and change your password"})
        else:
            return render(request,"s_forget.html",{"msg":"Email not found"})
    return render(request,"s_forget.html")

def s_change_password(request,email):
    if request.method=="POST":
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password==confirm_password:
            TutorRequest.objects.filter(email=email).update(password=password)
          
            
            return render(request,"login.html",{"msg":f"your password is changed!!!!! Start login"})
        else:
            return render(request,"s_c_p.html",{"msg":"password and confirm password not match"})
        


    return render(request,"s_c_p.html",{"email":email})




#new api


#show detail of teacher

def show_teacher(request,email):
    teacher=TutorRequest.objects.filter(email=email).first()
    all_tutor=TutorRegistration.objects.all()
    return render(request,"h_all_teacher.html",{"teacher":teacher,"tutors":all_tutor})



from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'


def common_dashboard(request):
    user = request.user if request.user.is_authenticated else None
    if TutorRequest.objects.filter(email=user.email).exists():
        return redirect("myposts")
    elif TutorRegistration.objects.filter(email=user.email).exists():
        return redirect("teacher_dashboard")
    else:
        return render(request,"home.html")      





    



      












    
    






       


    


                           





    
 

    

    





          


    













    