from pyexpat.errors import messages
from django.shortcuts import render ,redirect,HttpResponse ,HttpResponseRedirect
from app.models import Staff, Staff_Notification, Staff_Leave,Staff_Feedback
from django.contrib import messages

def HOME(request):
    return render(request,'Staff/home.html')


def NOTIFICATIONS(request):
    staff = Staff.objects.get(admin = request.user.id)
    notification  = Staff_Notification.objects.filter(staff_id = staff)
    context = {
      'notification' : notification,
    }
    return render(request,'Staff/notification.html',context)
  
def STAFF_NOTIFICATION_MARK_AS_DONE(request,status):
  notification = Staff_Notification.objects.get(id = status)
  notification.status = 1
  notification.save()
  messages.success(request,"Message Confirm")
  return redirect('notifications')

def STAFF_APPLY_LEAVE_SAVE(request):
  if request.method == "POST":
    leave_date = request.POST.get('leave_date')
    leave_message = request.POST.get('leave_message')
    staff = Staff.objects.get(admin = request.user.id)

    leave = Staff_Leave(
      staff_id = staff,
      data = leave_date,
      message = leave_message
    )
    leave.save()
    messages.success(request,"Leave Apply Successfully Sent:")
   
    return redirect('staff_apply_leave')


def STAFF_APPLY_LEAVE(request):
  staff = Staff.objects.filter(admin = request.user.id)
  for i in staff:
    staff_id = i.id
    staff_leave_history = Staff_Leave.objects.filter(staff_id = staff_id)

    context = {
      'staff_leave_history' : staff_leave_history,
    }
  
  return render(request,'Staff/apply_leave.html',context)


def STAFF_FEEDBACK(request):
  staff_id  =Staff.objects.get(admin=request.user.id)
  feedback_history = Staff_Feedback.objects.filter(staff_id = staff_id)
  context = {
    'feedback_history':feedback_history,
  }
  return render(request,'Staff/feedback.html',context)


def STAFF_FEEDBACK_SAVE(request):
  if request.method == "POST":
    feedback = request.POST['feedback']
    staff = Staff.objects.get(admin = request.user.id)
    feedback = Staff_Feedback(
      staff_id = staff,
      feedback = feedback
    )
    feedback.save()
    messages.success(request,"Feedback Send Sucessfully")
  return render(request,'Staff/feedback.html')

  
