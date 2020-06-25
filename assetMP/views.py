from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from assetMP.models import Employee_Table
from assetMP.models import Assets_Table
from assetMP.models import Assets_Employee_Table
from assetMP.models import Login_Table

granduser = 'default'
grandpassword = None
grandrole = None
grandid = None
granderror = None
password_message = None

def login1_view(request):
    error = None
    error_message = None
    print("login view is rendering")
    template_name = 'login1.html'
    if request.method == 'POST':
        print('Post data is: ')
        print(request.POST)
        id = request.POST.get("id")
        password = request.POST.get("pw")
        print(id,password)
        queryset = Login_Table.objects.filter(Userid__iexact = id )
        # emprow_queryset = Employee_Table.objects.filter(Employee_ID__iexact = empid)
        if queryset.exists():
            for row in queryset:
                if row.password == password:
                    global granduser, grandpassword, grandrole, grandid
                    grandid = id
                    grandpassword = password
                    grandrole = row.role
                    granduser = row.name
                    if row.role == 'Admin':
                        return HttpResponseRedirect('/admin-login')
                    else:
                        return HttpResponseRedirect('/employee-login')
                else:
                    error = True
                    error_message = "Password Incorrect"
        else:
            error = True
            error_message = "Username Doesnot Exists."
    context = {
        'error':error,
        'error_message':error_message
    }
    return render(request, template_name, context)

def admin_view(request):
    # return render(request,'admin.html',{})
    global granduser, grandpassword, grandrole, grandid, granderror, password_message
    user = granduser
    role = grandrole
    error_message = ''
    no_employee = True
    assetqueryset = Assets_Table.objects.all()
    assetempqueryset = Assets_Employee_Table.objects.all()
    empqueryset = Employee_Table.objects.all()
    loginqueryset = Login_Table.objects.all()
    # distinct_queryset = Assets_Employee_Table.objects.order_by().values('ASSETID','DEVICE','MANUFACTURE','SNO','WARRANTYEXPIRY').distinct()
    if grandid:
        print(type(grandid),grandid)
        for login_row in loginqueryset:
            print(login_row.Userid, type(login_row.Userid))
            print(login_row.password,type(login_row.password))
        if request.method == 'POST':
            if 'change-password' in request.POST:
                password_message = None
                old_password = request.POST.get('pw')
                new_password = request.POST.get('cpw')
                for  login_row in loginqueryset:
                    if login_row.Userid == int(grandid):
                        if login_row.password == old_password:
                            password_message= "password updated successfully"
                            obj = Login_Table.objects.filter(Userid__iexact = int(grandid)).update(
                                password = new_password
                            )
                        else:
                            password_message= "old password is incorrect"
                        return HttpResponseRedirect("/admin-login")
            if 'Logout' in request.POST:
                granduser = 'default'
                grandpassword = None
                grandrole = None
                grandid = None
                password_message = None
                return HttpResponseRedirect("/login")

            if 'addasset' in request.POST:
                password_message = None
                print('Post data')
                print(request.POST)
                assetid = request.POST.get("ass-id")
                device = request.POST.get("device")
                sno = request.POST.get("sno")
                mdate = request.POST.get("mdate")
                wdate = request.POST.get("wdate")
                for asset_row in assetqueryset:
                    print("asset-row is ")
                    if asset_row.ASSETID == assetid:
                        print('Asset with the asset ID ' + assetid + 'already exists')
                        granderror = 'Asset with same name already exists.'
                        print(granderror)
                        return HttpResponseRedirect("/admin-login")
                granderror=None
                obj = Assets_Table.objects.create(
                    ASSETID = assetid,
                    DEVICE = device,
                    MANUFACTURE = mdate,
                    SNO = sno,
                    WARRANTYEXPIRY = wdate,
                )
                print(assetid, device, sno, mdate, wdate)
                return HttpResponseRedirect("/admin-login")

            if 'assignform' in request.POST:
                password_message = None
                print('Post data')
                print(request.POST)
                firstname = request.POST.get("first-name")
                lastname = request.POST.get("last-name")
                empid = int(request.POST.get("empid"))
                email = request.POST.get("email")
                assetid = request.POST.get('assignform')
                granderror= ''
                print(type(empid))
                for emp_row in empqueryset:
                    if emp_row.Employee_ID == empid:
                        print("Employee Present in the employee database.")
                        no_employee = False
                        for assetemp in assetempqueryset:
                            if assetemp.Assetid == assetid and assetemp.Employeeid == empid:
                                granderror = "Employee Already has the Asset."
                                print(granderror)
                                return HttpResponseRedirect("/admin-login")
                        else:
                            obj = Assets_Employee_Table.objects.create(
                            Assetid = assetid,
                            Employeeid = empid
                            )
                            print("Asset added to employee")
                            return HttpResponseRedirect("/admin-login")
                else:
                    no_employee = True
                    granderror = "Employee Not present in the employee Database."
                    return HttpResponseRedirect("/admin-login")
                return HttpResponseRedirect("/admin-login")
    else:
        return HttpResponseRedirect("/login")
    context = {
        'granduser': user,
        'grandrole': role,
        'assettable': assetqueryset,
        # 'assettabled':distinct_queryset,
        'granderror': granderror,
        'error-message': error_message,
        'grandid':grandid,
        'password_message': password_message
    }
    return render(request,'admin-login.html',context)

def admin_employee_view(request):
    global granduser, grandpassword, grandrole, grandid, granderror, password_message
    user = granduser
    role = grandrole
    asset_present = False
    loginqueryset = Login_Table.objects.all()
    error_message = ''
    empqueryset = Employee_Table.objects.all()
    assetemptable = Assets_Employee_Table.objects.all()
    assettable = Assets_Table.objects.all()
    if grandid:
        if request.method == 'POST':
            if 'change-password' in request.POST:
                password_message = None
                old_password = request.POST.get('pw')
                new_password = request.POST.get('cpw')
                for  login_row in loginqueryset:
                    if login_row.Userid == int(grandid):
                        if login_row.password == old_password:
                            password_message= "password updated successfully"
                            obj = Login_Table.objects.filter(Userid__iexact = int(grandid)).update(
                                password = new_password
                            )
                        else:
                            password_message= "old password is incorrect"
                        return HttpResponseRedirect("/admin-employee")
            if 'Logout' in request.POST:
                granduser = 'default'
                grandpassword = None
                grandrole = None
                grandid = None
                password_message = None
                return HttpResponseRedirect("/login")
            granderror = None
            print('Post data')
            print(request.POST)
            Employee_ID = request.POST.get("emp-id")
            First_Name = request.POST.get("first-name")
            Last_Name = request.POST.get("last-name")
            Employee_Email = request.POST.get("email")
            for empobj in empqueryset:
                if empobj.Employee_ID == int(Employee_ID):
                    print("A employee already exists with same empid in the database.")
                    granderror = "A employee already exists in the database."
                    return HttpResponseRedirect("/admin-employee")
            else:
                obj = Employee_Table.objects.create(
                    Employee_ID = Employee_ID,
                    First_Name = First_Name,
                    Last_Name = Last_Name,
                    Employee_Email = Employee_Email
                )
                obj1 = Assets_Employee_Table.objects.create(
                    Assetid = 'AS001',
                    Employeeid = Employee_ID
                )
            print(Employee_ID, First_Name, Last_Name, Employee_Email)
            return HttpResponseRedirect("/admin-employee")
        context = {
            'granduser':user,
            'grandrole':role,
            'employeetable': empqueryset,
            'assettable':assettable,
            'assetemptable':assetemptable,
            'granderror':granderror,
            'asset_present': asset_present,
            'password_message':password_message
            # 'employeerow':emprow,
        }
        return render(request,'admin-employee.html',context)
    else:
        return HttpResponseRedirect("/login")


def employee_view(request):
    global granduser, grandpassword, grandrole, grandid, password_message
    template_name = 'employee-login.html'
    loginqueryset = Login_Table.objects.all()
    if grandid:
        print(grandid)
        grandid = int(grandid)
        empqueryset = Employee_Table.objects.filter(Employee_ID__iexact = grandid)
        assetempqueryset = Assets_Employee_Table.objects.all()
        assetqueryset = Assets_Table.objects.all()
        asset_dict = []
        for assetemp in assetempqueryset:
            print('for started')
            print(type(grandid),type(assetemp.Employeeid))
            if assetemp.Employeeid == int(grandid):
                print("Employee is present.")
                for asset in assetqueryset:
                    if asset.ASSETID == assetemp.Assetid:
                        print("Asset present")
                        asset_dict.append(
                            {
                                'Assetid':asset.ASSETID,
                                'Device':asset.DEVICE
                            }
                        )
        print('assets dic is: ',asset_dict)
        if request.method == 'POST':
            if 'change-password' in request.POST:
                password_message = None
                old_password = request.POST.get('pw')
                new_password = request.POST.get('cpw')
                for  login_row in loginqueryset:
                    if login_row.Userid == int(grandid):
                        if login_row.password == old_password:
                            password_message= "password updated successfully"
                            obj = Login_Table.objects.filter(Userid__iexact = int(grandid)).update(
                                password = new_password
                            )
                        else:
                            password_message= "old password is incorrect"
                        return HttpResponseRedirect("/employee-login")
            if 'Logout' in request.POST:
                granduser = 'default'
                grandpassword = None
                grandrole = None
                grandid = None
                password_message = None
                return HttpResponseRedirect("/login")
        if empqueryset:
            message = 'Employee Data Exists in database.'
            print(message)
        else:
            message = 'Employee Data is not present in the database'
            print(message)
    else:
        return HttpResponseRedirect("/login")
    context = {
        'empqueryset':empqueryset,
        'assetqueryset':assetqueryset,
        'assetempqueryset': assetempqueryset,
        'messsage':message,
        'granduser':granduser,
        'grandrole':grandrole,
        'asset_dict':asset_dict,
        'password_message':password_message,
         'userid': int(grandid)
    }
    return render(request, template_name,context)

