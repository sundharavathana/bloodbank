from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from .models import Donordetail, userdetail, patientdata, patientuser
from django.shortcuts import redirect, get_object_or_404


def home(request):
    items = [
        {"title": "Are you a Donor?", "btn": "Click here", "link": reverse('bloodbankapp:signup')},
        {"title": "Are you a Patient?", "btn": "Click here", "link": reverse('bloodbankapp:p_signup')}, 
    ]
    data=[
        {
            "img":'images/O-.jpg',"donate":"Everyone(universal donor)" ,"receive":"O-"
        },
          {
            "img":'images/OF.jpg',"donate":"O+, A+, B+, AB+" ,"receive":"O-, O+"
        },
          {
            "img":'images/A-.jpg',"donate":"A+, A-, AB+, AB-" ,"receive":"O-, A-"
        },
        {
            "img":'images/AF.jpg',"donate":"A+, AB+" ,"receive":"O-, O+, A+, A-"
        },
        {
            "img":'images/B-.jpg',"donate":"B+, B-, AB+, AB-" ,"receive":"O-, B-"
        },
        {
            "img":'images/BF.jpg',"donate":"B+, AB+" ,"receive":"O-, B-, B+, O+"
        },
        {
            "img":'images/AB-.jpg',"donate":"AB+, AB-" ,"receive":"O-, A-, B-, AB-"
        },
        {
            "img":'images/AB.jpg',"donate":"AB+" ,"receive":"Everyone(Universal Recipent)"
        }

    ]
    context={ "items": items ,"data":data}
 
    
    return render(request, 'home.html',context)



def signup(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_pass = request.POST.get('confirm_pass')

        if userdetail.objects.filter(email=email).exists():
            error = "Email is already registered!"
        elif userdetail.objects.filter(username=username).exists():
            error = "Username is already taken!"
        elif password != confirm_pass:
            error = "Passwords do not match!"
        else:
            hash_password = make_password(password)
            userdetail.objects.create(username=username, email=email, password=hash_password)
            return redirect('bloodbankapp:login')

    return render(request, 'donor/register.html', {'error': error})



def login(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = userdetail.objects.get(email=email)
        except userdetail.DoesNotExist:
            user = None

        if user and check_password(password, user.password):
            request.session['donor_id'] = user.id
            return redirect('bloodbankapp:donordetails')
        else:
            error = "Invalid email or password."

    return render(request, 'login.html', {'error': error})



def donordetails(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        patient = patientdata.objects.filter(pk=patient_id).first() if patient_id else None

        donor = Donordetail(
            username=request.POST.get('username'),
            gender=request.POST.get('gender'),
            age=int(request.POST.get('age') or 0),
            bloodgroup=request.POST.get('bloodgroup'),
            rhoptions=request.POST.get('rhoptions'),
            unit=int(request.POST.get('unit') or 0),
            location=request.POST.get('location'),
            patient=patient,
            idproof=request.FILES.get('idproof'),
            mc=request.FILES.get('mc'),
            image=request.FILES.get('image')
        )
        donor.save()

        return redirect(reverse('bloodbankapp:success') + (f'?patient_id={patient_id}' if patient_id else ''))

   
    patients = patientdata.objects.all()
    return render(request, 'donor/dashboard.html', {'data': patients})



def p_signup(request):
    error = None
    if request.method == 'POST':
        p_name = request.POST.get('p_name')
        p_email = request.POST.get('p_email')
        p_password = request.POST.get('p_password')
        confirm_pass = request.POST.get('confirm_pass')

        if patientuser.objects.filter(p_email=p_email).exists():
            error = "Email already registered!"
        elif patientuser.objects.filter(p_name=p_name).exists():
            error = "Username already taken!"
        elif p_password != confirm_pass:
            error = "Passwords do not match!"
        else:
            hash_password = make_password(p_password)
            patientuser.objects.create(p_name=p_name, p_email=p_email, p_password=hash_password)
            return redirect('bloodbankapp:patientdetails')

    return render(request, 'patient/patientreg.html', {'error': error})



def p_login(request):
    error = None
    if request.method == 'POST':
        p_email = request.POST.get('p_email')
        p_password = request.POST.get('p_password')

        try:
            user = patientuser.objects.get(p_email=p_email)
        except patientuser.DoesNotExist:
            user = None

        if user and check_password(p_password, user.p_password):
            patient = patientdata.objects.filter(name=user.p_name).first()
            if patient:
                # ✅ Existing patient → go to dashboard
                request.session['patient_id'] = patient.id
                return redirect('bloodbankapp:patient_dashboard')
            else:
                # ✅ New patient → go fill details
                request.session['pending_name'] = user.p_name
                return redirect('bloodbankapp:patient_dashboard')
        else:
            error = "Invalid email or password."

    return render(request, 'patientlogin.html', {'error': error})




def patientdetails(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        bloodgroup = request.POST.get('bloodgroup')
        rhoptions = request.POST.get('rhoptions')
        unit = request.POST.get('unit')
        location = request.POST.get('location')
        hospital = request.POST.get('hospital')
        ifany = request.POST.get('ifany')

        patient = patientdata.objects.create(
            name=name,
            age=age,
            bloodgroup=bloodgroup,
            rhoptions=rhoptions,
            gender=gender,
            unit=unit,
            location=location,
            hospital=hospital,
            ifany=ifany
        )

        request.session['patient_id'] = patient.id
        if 'pending_name' in request.session:
            del request.session['pending_name']

        return redirect('bloodbankapp:p_login')

    return render(request, 'patient/patientdetails.html')



def success(request):
    patient_name = None
    patient_id = request.GET.get('patient_id')

    if patient_id:
        patient = patientdata.objects.filter(pk=patient_id).first()
        patient_name = patient.name if patient else None

    return render(request, 'success.html', {'patient_name': patient_name})


def patient_dashboard(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('bloodbankapp:p_login')

    try:
        patient = patientdata.objects.get(id=patient_id)
    except patientdata.DoesNotExist:
        return HttpResponse("Patient data not found. Please fill in your details.")

    donors = Donordetail.objects.filter(patient=patient)
    return render(request, 'patient/patient_dashboard.html', {'patient': patient, 'donors': donors})

def adminview(request):
    data = Donordetail.objects.select_related('patient').filter(patient__isnull=False)
    return render(request, 'admin.html', {'data': data})








def approve_patient(request, patient_id):
    patient = get_object_or_404(patientdata, id=patient_id)

    
    patient.delete()

    return redirect('bloodbankapp:adminview') 
