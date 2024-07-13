from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Employee
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

def index(request):
        return render(request, 'index.html')


def all_emp(request):
  latest_emp = Employee.objects.order_by('-id')[0:1]
  remaining_emps = Employee.objects.all().exclude(id=latest_emp.first().id)
  emps = list(latest_emp) + list(remaining_emps)  # Combine lists
  context = {
      'emps': emps
      }
  return render(request, 'all_emp.html', context)





def add_emp(request):
    if request.method == 'POST':
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        department_name = request.POST.get('department_name')
        role = request.POST.get('role')
        try:
            salary = int(request.POST.get('salary'))
        except ValueError:
            return HttpResponse("Invalid salary value")

        new_emp = Employee(first_name=first_name, last_name=last_name, department_name=department_name, role=role, salary=salary)
        new_emp.save()
        emps = Employee.objects.all()
        context = {
            'emps': emps
        }
        messages.success(request, "New Employee Added Successfully!")
        return redirect('all_emp')
        # return render(request, 'all_emp.html', context)
    else:
        return render(request, 'add_emp.html')
    
    
    

def remove_emp(request, emp_id = 0):
    if emp_id:
        try:
            emptoberemoved = Employee.objects.get(id=emp_id)
            emptoberemoved.delete()
            emps = Employee.objects.all()
            context = {
                'emps': emps
            }
            messages.success(request, " Employee Removed Successfully!")
            return render(request, 'all_emp.html', context)
        except:
            return HttpResponse('Select valid employee id')



def select_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'select_emp.html', context)




def edit_emp(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        department_name = request.POST.get('department_name')
        role = request.POST.get('role')
        salary = request.POST.get('salary')
        
        if first_name:
            employee.first_name = first_name
        if last_name:
            employee.last_name = last_name
        if department_name:
            employee.department_name = department_name
        if role:
            employee.role = role
        if salary:
            try:
                employee.salary = int(salary)
            except ValueError:
                return HttpResponse("Invalid salary value")

        employee.save()
        
        return redirect('all_emp')
    else:
        context = {
            'employee': employee
        }
        messages.success(request, "Employee Details Edited Successfully!")
        return render(request, 'edit_emp.html', context)
    

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username = username).exists():
            messages.warning(request, "Invalid Username")
            return redirect('login_user')
        
        user = authenticate(request, username = username, password = password) 
       
        if user is None:
            messages.warning(request, "Invalid Password")
            return redirect('login_user')

        login(request, user)
        return redirect('index')
    
    return render(request, 'login_user.html')




def logout_user(request):
    logout(request)
    # return render(request, 'index.html')
    return redirect('index')




def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(username=username)
        if user.exists():
            messages.warning(request, "This username already exists!")
            return redirect('signup')
    
        
        user = User.objects.create_user(
            username = username
        )
        
        user.set_password(password)
        user.save()
        messages.success(request, "New User Created Successfully!")
        return redirect('index')
        
    return render(request, 'signup.html')