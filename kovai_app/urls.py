from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import (
   
    CustomPasswordResetView, CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView)
urlpatterns = [
 path('',views.mains, name='mains'),
 path('tutor_request',views.tutor_request, name='tutor_request'),
 path('otp_verify/<email>',views.otp_verify, name='otp_verify'),
 path('email_verify/<email>',views.email_verify, name='email_verify'),
 path('add_post/<email>',views.addpost, name='addpost'),
 path('myposts/', views.myposts, name='myposts'),
 path('mypost/<str:email>/', views.mypost, name='mypost'),
 path('delete_post/<int:id>',views.delete_posst, name='delete_posst'),
 path('stu_login',views.stu_login, name='stu_login'),
  path('delete_stu',views.delete_stu, name='delete'),

#path('search_teachers/<email>',views.search_teachers, name='search_teachers'),
path('online_tutors/<email>',views.online_tutor, name='online_tutors'),
path('home_tutors/<email>',views.home_tutor, name='home_tutor'),
 path('fliter_location/<location>/<email>',views.fliter_location, name='fliter_location'),
path('student_inbox/<email>',views.student_inbox, name='student_inbox'),
path('student_post/<email>/<int:id>',views.student_post, name='student_post'),
 #teacher_________________________________________________________
  path('teacher_dashboard/',views.teacher_dashboard, name='teacher_dashboard'),

  path('teacher_reg',views.teacher_reg, name='teachet_reg'),
  path('details',views.details, name='details'),
  path('subject/<email>',views.subject, name='subject'),
path('add_subject/<email>',views.addsubject, name='addsubject'),
  path('certificate/<email>',views.certificate, name='certificate'),
    path('add_certificate/<email>',views.addcertificate, name='addcertificate'),
     path('company_emp/<email>',views.company_emp, name='company_emp'),
      path('teaching_detail/<email>',views.teaching_detail, name='teaching_deatils'),
    path('personal_detail/<email>',views.personal_detail, name='personal_details'),
       path('teacher_email_verifed/<email>',views.teacher_email_verifed, name='teacher_email_verified'),
         path('teacher_login',views.teach_login, name='teach_login'),
          path('myprofile/<email>',views.myprofile, name='myprofile'),
           #path('search_teacher/<email>',views.search_teacher, name='search_teacher'),

          # path('fliter_location/<location>/',views.fliter_location, name='fliter_location'),

          #  path('online_tutor',views.online_tutor, name='online_tutors'),
          #   path('home_tutor',views.home_tutor, name='home_tutors'),
            
            

              
               path('stu_settings/<email>',views.stu_settings, name='stu_settings'),
               path('student_profile/<email>',views.student_profile, name='student_profile'),
              path('change_e/<email>',views.change_e, name='change_e'),
               path('change_ph/<email>',views.change_ph, name='change_ph'),
              path('otp_verify_teacher/<email>',views.otp_verify_teacher, name='otp_verify_teacher'),

               # edit teacher
               path('t_basic/<email>',views.t_basic, name='t_basic'),
               path('t_photo/<email>',views.t_photo, name='t_photo'),
                 path('t_subject/<email>',views.t_subject, name='t_subject'),
                  path('t_contact/<email>',views.t_contact, name='t_contact'),
                   path('change_p/<email>',views.change_p, name='change_p'),
                   path('t_teaching/<email>',views.t_teaching, name='t_teaching'),
                   path('t_experience/<email>',views.t_experience, name='t_experience'),

                #search job

                #  path('search_job',views.search_job, name='search_job'),
                #   path('search_jobs/<email>',views.search_jobs, name='search_jobs'),
                 path('search_jobs',views.search_jobs, name='search_jobs'),
                  path('tutor_job/<email>',views.tutors_job, name='tutors_job'),
                   path('tutor_online_job/<email>',views.tutors_online_job, name='tutors_job'),
                    path('h_all_teachers',views.h_all_teachers, name='h_all_teachers'),
                     path('h_online_tutor',views.h_online_tutor, name='h_online_tutor'),
                      path('h_home_tutor',views.h_home_tutor, name='h_home_tutor'),
                     # path('h_fliter_location/<str:location>/', views.h_fliter_location, name='h_fliter_location'),

                       path('h_tutors_job', views.h_tutors_job, name='h_tutors_job'),

                path('h_online_job', views.h_online_job, name='h_online_job'),
                path('h_home_job', views.h_home_job, name='h_home_job'),
                 path('h_search_teacher',views.h_search_teacher, name='h_search_teacher'),
                 path('t_wallet/<email>',views.t_wallet, name='t_wallet'),
                 path('buy_coin_teach/<email>/<int:coins>',views.buy_coin_teach, name='buy_coin_teach'),
                 path('view_post_teach/<a_email>/<email>/<int:id>',views.view_post_teach, name='view_post_teach'),
                 path('use_coin_teach/<a_email>/<email>/<int:id>',views.use_coin_teach, name='use_coin_teach'),


                 path('t_message_to/<s_email>/<r_email>',views.t_message_to, name='t_message_to'),
                   path('teacher_inbox/<email>',views.teacher_inbox, name='t_message_to'),
                    path('s_wallet/<email>',views.s_wallet, name='s_wallet'),
                   
                    path('buy_coin_stu/<email>/<int:coins>',views.buy_coin_stu, name='tbuy_coin_stu'),
                    path('student_update/<email>/<int:id>',views.student_update, name='student_update'),
 path('s_myprofile/<email>/<s_email>',views.s_myprofile, name='s_myprofile'),
 path('view_message_stu/<a_email>/<email>/<int:id>',views.view_message_stu, name='s_myprofile'),
 path('view_contact_stu/<a_email>/<email>/<int:id>',views.view_contant_stu, name='iew_contant_stu'),
  path('use_coin_view_contant_stu/<a_email>/<email>/<int:id>',views.use_coin_view_contant_stu, name='use_coin_view_contant_stu'),

 path('home',views.home, name='home'),
 path('delete_all',views.delete_all, name='delete_all'),
 path('t_forget_password',views.t_forget_password, name='t_forget_password'),
  path('s_forget_password',views.s_forget_password, name='s_forget_password'),  
  path('change_password/<email>',views.change_password, name='change_password'),
  path('s_change_password/<email>',views.s_change_password, name='s_change_password'),      
  path('about',views.about, name='about'),              



  #new api show teacher

   path('show_teacher/<email>',views.show_teacher, name='show_teacher'), 
        
                     

path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('logout/', LogoutView.as_view(next_page='stu_login'), name='logout'),            

 path('buy_coin_stus/<int:amount>',views.buy_coin_stus, name='tbuy_coin_stu'),
 path('payment/verify/', views.verify_payment, name='verify_payment'),

 path('buy_coin_teacher/<int:amount>',views.buy_coin_teacher, name='buy_coin_teacher'),
 path('payment/verify_teacher/', views.verify_payment_teacher, name='verify_payment'),
  path('common_dashboard', views.common_dashboard, name='Dashboard'),
  
 path('policy', views.policy, name='Dashboard'),



   


   




]
