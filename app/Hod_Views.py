from multiprocessing import context
from django.shortcuts import render ,redirect,HttpResponse ,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from app.models import Course,Session_Year, Staff_Leave, Student ,CustomUser,Staff, Subject,Staff_Notification,Staff_Feedback
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='/')
def HOME(request):
    #if request.user.is_authenticated:
       student_count = Student.objects.all().count()
       staff_count = Staff.objects.all().count()
       course_count = Course.objects.all().count()
       subject_count = Subject.objects.all().count()
       student_gender_male = Student.objects.filter(gender = 'Male').count()
       student_gender_female = Student.objects.filter(gender = 'Female').count()
      
       context = {
        'student_count' : student_count,
        'staff_count' : staff_count,
        'course_count' : course_count,
        'subject_count' : subject_count,
        'student_gender_male' : student_gender_male,
        'student_gender_female' : student_gender_female

       }
      
       return render(request,'Hod/home.html',context)
   # else:
    #     return redirect('login')

@login_required(login_url='/')
def ADD_STUDENT(request):
    course = Course.objects.all()
    session_year = Session_Year.objects.all()
    context={
        'course':course,
        'session_year':session_year,
    }
    if request.method == "POST" :
        try:
            profile_pic = request.FILES.get('profile_pic')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            address = request.POST.get('address')
            gender = request.POST.get('gender')
            course_id = request.POST.get('course_id')
            session_year_id = request.POST.get('session_year_id')

            if CustomUser.objects.filter(email=email).exists():
                messages.warning(request,"Email is Already Taken")
                return redirect('add_student')
            else:
                user = CustomUser(
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    username = username,
                    profile_pic = profile_pic,
                    user_type = 3
                )
                user.set_password(password)
                user.save()
                course = Course.objects.get(id=course_id)
                session_year = Session_Year.objects.get(id=session_year_id)
                student = Student(
                    admin = user,
                    address = address,
                    course_id = course,
                    gender = gender,
                    session_year_id = session_year,

                )
                student.save()
                messages.success(request,user.first_name + " " +user.last_name + " Are Successfully Added")
        except ValueError as d:
            messages.warning(request,d)

            return redirect('add_student')        
    return render(request,'Hod/add_students.html', context)


#VIEW STUDENT TABEL
@login_required(login_url='/')
def VIEW_STUDENT(request):
    student = Student.objects.all()
    context = {
        'student' : student,
    }
    return render(request,'Hod/view_student.html',context)


#EDIT STUDENT
@login_required(login_url='/')
def EDIT_STUDENT(request,id):
    student = Student.objects.filter(id=id)
    course = Course.objects.all()
    session_year = Session_Year.objects.all()
    context = {
        'student' : student,
        'course' :course,
        'session_year' : session_year
    }
    return render(request,'Hod/edit_student.html',context)

#UPDATE STUDENT
@login_required(login_url='/')
def UPDATE_STUDENT(request):
    if request.method == 'POST':
        try:
            student_id = request.POST.get('student_id')
            profile_pic = request.FILES.get('profile_pic')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            address = request.POST.get('address')
            gender = request.POST.get('gender')
            course_id = request.POST.get('course_id')
            session_year_id = request.POST.get('session_year_id')
        except ValueError as v:
            print("Please select currect value",v)
        
        else:

        #CustomUser Model Object Create user
            user = CustomUser.objects.get(id=student_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.user_type =3
            if password !=None and password !="":
                    user.set_password(password)
            if profile_pic !=None and profile_pic !="":
                    user.profile_pic = profile_pic
            user.save()

        #Student Model Object Create student
            student = Student.objects.get(admin=student_id)
            student.address = address
            student.gender = gender
            try:
                course = Course.objects.get(id=course_id)
                student.course_id = course
                session_year = Session_Year.objects.get(id=session_year_id)
                student.session_year_id =session_year
            except:
                print("some Erorr")
            else:

              student.save()
              messages.success(request,"Record Are Successfully Updated !")
              return redirect('view_student')      
    return render(request,'Hod/edit_student.html')

# DELETE STUDENT
@login_required(login_url='/')
def DELETE_STUDENT(request,id):
    try:
        student = CustomUser.objects.get(id=id)
        if student.is_superuser:
           return JsonResponse({'status':403,'message':'You cannot delete An Admin'})
        else:            
           student.delete()
       #return JsonResponse({'status':200,'message':'Record Are Successfully Deleted '})
           messages.success(request,"Record Are Successfully Deleted !")
           return redirect('view_student') 
    except CustomUser.DoesNotExist:
         return JsonResponse({'status':404,'message':'Record Not AVailable '})



#=========================================================================
#Add Couse
@login_required(login_url='/')
def ADD_COURSE(request):
    if request.method == "POST":
        try:
            course_name = request.POST.get('course_name')
            en = Course(name=course_name)
            en.save()     
            messages.success(request,"Course :"+course_name+ " Are Successfully Created")     
            #return HttpResponseRedirect(reverse("add_course"))  
            # OR
            return redirect('add_course')    
        except ValueError as d:
            messages.warning(request,d)
    return render(request,"Hod/add_course.html")

# View Course
@login_required(login_url='/')
def VIEW_COURSE(request):
    course = Course.objects.all()
    context = {
        'course' :course,
    }
    return render(request,"Hod/view_course.html",context)

# EDIT COURSE
@login_required(login_url='/')
def EDIT_COURSE(request,id):
    course = Course.objects.get(id=id)
    context = {
        'course':course
    }
    return render(request,"Hod/edit_course.html",context)

#Update Course   
@login_required(login_url='/')
def UPDATE_COURSE(request):
    if request.method == "POST":
        try:
            course_id = request.POST['course_id']
            course_name = request.POST['course_name']
            course = Course.objects.get(id=course_id)
            old_course_name =course.name
            course.name = course_name
            course.save()
            messages.success(request,"{}:To {}:Course Are Successfully Updated !".format(old_course_name,course_name))
            return redirect('view_course')
        except:
            print("PLease Check UPDATe COurse")
    return render(request,"Hod/edit_course.html")

@login_required(login_url='/')
def DELETE_COURSE(request,id):
    try:
        course = Course.objects.get(id=id)
        delete_course_name = course.name
        course.delete()
        #return JsonResponse({'status':200,'message':'Record Are Successfully Deleted '})
        #Or
        messages.success(request,"{}:Course Are Succesfully Deteled".format(delete_course_name))
        return redirect('view_course')
    
    except Course.DoesNotExist:
         messages.success(request,"Course Are NOt Found Created") 
@login_required(login_url='/')        
def ADD_STAFF(request):
    if request.method == "POST":
        try:
            profile_pic = request.FILES.get('profile_pic')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            address = request.POST.get('address')
            gender = request.POST.get('gender')
            if CustomUser.objects.filter(email=email).exists():
                messages.warning(request,"Email is Already Taken")
                return redirect('add_student')
            else:
               user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                user_type = 2
               )
               user.set_password(password)
               user.save()

               staff = Staff(
                admin = user,
                gender = gender,
                address = address
               )
               staff.save()
               messages.success(request,user.first_name + " " +user.last_name + " Are Successfully Added")
        except ValueError as s:
            messages.warning(request,"Please staff error",s)
    return render(request,"Hod/add_staff.html")

#VIew Staff List
@login_required(login_url='/')
def VIEW_STAFF(request):
    staff = Staff.objects.all()
    context ={
        'staff':staff
    }
    
    return render(request,"Hod/view_staff.html",context)

@login_required(login_url='/')
def EDIT_STAFF(request,id):
    staff = Staff.objects.filter(id=id)
    context ={
        'staff' : staff,
    }
    
    return render (request,"Hod/edit_staff.html",context)

@login_required(login_url='/')
def UPDATE_STAFF(request):
    if request.method == "POST":
        try:
            staff_id = request.POST.get('staff_id')
            profile_pic = request.FILES.get('profile_pic')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            address = request.POST.get('address')
            gender = request.POST.get('gender')
        except ValueError as v:
            print("Please select currect value",v)
        
        else:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.user_type = 2
            if password !=None and password !="":
                user.set_password(password)
            if profile_pic !=None and profile_pic !="":
                user.profile_pic = profile_pic
            user.save()

            staff =Staff.objects.get(admin=staff_id)
            staff.address = address
            staff.gender = gender
            staff.save()
            messages.success(request,"Record Are Successfully Updated !")
            return redirect('view_staff')      
    return render(request,'Hod/edit_staff.html')

    # DELETE
#@csrf_exempt
@login_required(login_url='/')
def DELETE_STAFF(request,id):
    try:
        staff = CustomUser.objects.get(id=id)
        staf_name = staff.username
        print(staff.username)
        print(staff.user_type)
        
        if staff.is_superuser:
            return JsonResponse({'status':403,'message':'You cannot delete An Admin'})
        if staff.user_type=='3':
             print(staff.user_type)
             return JsonResponse({'status':403,'message':'You cannot delete A Student'})
        else:
            staff.delete()
            #return JsonResponse({'status':200,'message':'User {} Are Successfully Deleted'.format(staf_name)})
            messages.success(request,"{} Are deleted in Your Staff List".format(staf_name))
            #return redirect('view_staff')
            return render(request,'Hod/view_staff.html')
            #return HttpResponseRedirect(reverse("view_staff"))

    except CustomUser.DoesNotExist:
        return JsonResponse({'status':200,'message':'Record Not Found  '})
         #messages.success(request,"Course Are NOt Found Created")

    
#===============================================================================
     

@login_required(login_url='/')
def ADD_SUBJECT(request):
    course  = Course.objects.all()
    staff = Staff.objects.all()
    context = {
        'course' : course,
        'staff' : staff,
    }
    if request.method == "POST":
        name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')
        print(name,course_id,staff_id)

        course = Course.objects.get(id=course_id)
        staff = Staff.objects.get(id=staff_id)
        subject  =Subject(name = name , course = course,staff = staff)
        subject.save()
        messages.success(request,"Subject:{} is Successfully Added".format(name))
        return redirect('add_subject')
    return render(request,'Hod/add_subject.html',context) 

#SUBJECT VIEW
@login_required(login_url='/')
def VIEW_SUBJECT(request):
    subject  =Subject.objects.all()
    context = {
        'subject':subject,
    }
    return render(request,'Hod/view_subject.html',context) 

@login_required(login_url='/')
def EDIT_SUBJECT(request,id):
    subject = Subject.objects.get(id=id)
    course  = Course.objects.all()
    staff = Staff.objects.all()
    context = {
        'course' : course,
        'staff' : staff,
        'subject':subject,
    }
    return render(request,'Hod/edit_subject.html',context)

@login_required(login_url='/')
def UPDATE_SUBJECT(request,id):
    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        course_id  = request.POST.get('course_id')
        staff_id  = request.POST.get('staff_id')
        
        course = Course.objects.get(id = course_id)
        staff  =Staff.objects.get(id = staff_id)
        print("1",course)
        subject = Subject.objects.get(id=id)
        subject.name = subject_name
        subject.course = course
        subject.staff  =staff
        subject.save()
        messages.success(request, "Subject Are Succeffully Updated")
        return redirect('view_subject')
    
   
    return render(request,'Hod/edit_subject.html',context)

@login_required(login_url='/')
def DELETE_SUBJECT(request,id):
    subject  = Subject.objects.get(id=id)
    subject.delete()
    messages.success(request, "{} are Successfully Deleted".format(subject))
    return redirect('view_subject')

#SESSION
@login_required(login_url='/')
def ADD_SESSION(request):
    if request.method == "POST":
        session_year_start = request.POST.get("session_year_start")
        session_year_end = request.POST.get("session_year_end")
        print(session_year_start,session_year_end)
        session_year  =Session_Year(
            session_start  = session_year_start,
            session_end= session_year_end,
        )
        session_year.save()
        messages.success(request, "{} TO {} is Successfully Added".format(session_year_start,session_year_end))
        return redirect('view_session')
    return  render(request, "Hod/add_session.html")
    

@login_required(login_url='/')
def VIEW_SESSION(request):
    session_year = Session_Year.objects.all()
    context = {
        'session_year' : session_year,
    }
    return  render(request, "Hod/view_session.html",context)


@login_required(login_url='/')
def EDIT_SESSION(request,id):
    session_year = Session_Year.objects.filter(id=id)
    context = {
        'session_year' : session_year,
    }
   
    return render(request,"Hod/edit_session_year.html",context)

@login_required(login_url='/')
def UPADETE_SESSION(request,id):
    if request.method == "POST":
        session_year = Session_Year.objects.get(id=id)
        session_year_start = request.POST.get("session_year_start")
        session_year_end = request.POST.get("session_year_end")
        session_year.session_start =session_year_start
        session_year.session_end = session_year_end
        session_year.save()
        messages.success(request, "{} TO {} is Successfully Updated".format(session_year_start,session_year_end))
        return redirect('view_session')

@login_required(login_url='/') 
def DELETE_SESSION(request,id):
    session  = Session_Year.objects.get(id=id)
    session_disp = session
    session.delete()
    messages.success(request, "{} are Successfully Deleted".format(session_disp))
    return redirect('view_session')

@login_required(login_url='/')
def STAFF_SEND_NOTIFICATION(request):
    staff = Staff.objects.all()
    see_notification = Staff_Notification.objects.all().order_by('-id')[0:5]
    context = {
        'staff' :staff,
        'see_notification' : see_notification,
    }
    return render(request,'Hod/staff_notification.html',context)

@login_required(login_url='/')
def SAVE_STAFF_NOTIFICATION(request):
    if request.method == "POST":
        message = request.POST.get('message')
        staff_id = request.POST.get('staff_id')
        staff  = Staff.objects.get(admin = staff_id)
        fname  = staff.admin.first_name
        lname = staff.admin.last_name
        notification = Staff_Notification(
            staff_id = staff,
            message = message
        )
        notification.save()
        messages.success(request,'Notification Succeessfully Sent TO {} {}'.format(fname,lname))
    return redirect('staff_send_notification')


#STAFF LEAVE VIEW

@login_required(login_url='/')
def STAFF_LEAVE_VIEW(request):
    staff_leave_view = Staff_Leave.objects.all()
    context = {
        'staff_leave_view' : staff_leave_view,
    }
    return render(request,"Hod/staff_leave.html",context)


#Approve Leave
@login_required(login_url='/')
def STAFF_APPROVE_LEAVE(request,id):
    leave = Staff_Leave.objects.get(id=id)
    leave.status = 1
    leave.save()
    messages.success(request,"Leave Successfully Approved")
    return redirect('staff_leave_view')

@login_required(login_url='/')
def STAFF_DISAPPROVE_LEAVE(request,id):
    leave = Staff_Leave.objects.get(id=id)
    leave.status = 2
    leave.save()
    messages.success(request,"Leave Successfully DisApproved")
    return redirect('staff_leave_view')

def STAFF_FEEDBACK(request):
    feedback = Staff_Feedback.objects.all()
    context ={
        'feedback':feedback,
    }

    return render(request,'Hod/staff_feedback.html',context)
        
    

    
    


        

