
from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.utils.text import slugify
from django.db.models import Q
from datetime import datetime
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import FileResponse, Http404, HttpResponse


def _write_case_pdf(receipe):
    """Render the case sheet template to PDF and save under MEDIA_ROOT/case_sheets/{slug}_{case}.pdf
    Returns the filepath."""
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if not media_root:
        media_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'media')

    folder = os.path.join(media_root, 'case_sheets')
    os.makedirs(folder, exist_ok=True)

    name_slug = slugify(receipe.receipe_name) if receipe.receipe_name else 'unknown'
    case_slug = slugify(receipe.case_number) if receipe.case_number else datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{name_slug}_{case_slug}.pdf"
    filepath = os.path.join(folder, filename)

    # Render HTML
    html = render_to_string('home/case_sheet.html', {'receipe': receipe, 'now': datetime.now().strftime('%Y-%m-%d %H:%M')})

    # Write PDF
    with open(filepath, 'wb') as f:
        pisa_status = pisa.CreatePDF(src=html, dest=f)
        if pisa_status.err:
            raise Exception('Error creating PDF')

    return filepath


def _remove_old_case_file(old_name, old_case):
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if not media_root:
        media_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'media')
    def _name_to_path(name, case):
        base = slugify(name) if name else 'unknown'
        if case:
            fname = f"{base}_{slugify(case)}.pdf"
        else:
            fname = f"{base}.pdf"
        return os.path.join(media_root, 'case_sheets', fname)

    old_path = _name_to_path(old_name, old_case)
    if os.path.exists(old_path):
        try:
            os.remove(old_path)
        except Exception:
            pass

# Create your views here.

@login_required(login_url="/login/")
def receipes(request):
    if request.method == "POST":
        data = request.POST
        try:
            print('update_receipe POST headers:', {k: v for k, v in request.META.items() if k.startswith('HTTP_')})
        except Exception:
            pass
        print('update_receipe POST keys:', list(data.keys()))
 
        case_number = data.get("case_number")
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        age = data.get('age')
        date = data.get('date')
        follow_up_date = data.get('follow_up_date')
        # normalize date inputs to date objects (if provided in YYYY-MM-DD)
        try:
            if date:
                date = datetime.strptime(date, '%Y-%m-%d').date()
        except Exception:
            # leave as-is; model will coerce or reject
            pass
        try:
            if follow_up_date:
                follow_up_date = datetime.strptime(follow_up_date, '%Y-%m-%d').date()
        except Exception:
            pass
        relation = data.get('relation')
        gender = data.get('gender')
        status = data.get('status')
        phone = data.get('phone')
        religion = data.get('religion')
        occupation = data.get('occupation')
        address = data.get('address')
        medical_history = data.get('medical_history')
        family_history = data.get('family_history')
        investigation = data.get('investigation')
        # personal history
        appetite = data.get('appetite')
        thirst = data.get('thirst')
        cravings = data.get('cravings')
        aversions = data.get('aversions')
        bowel_habits = data.get('bowel_habits')
        urine = data.get('urine')
        sleep_field = data.get('sleep')
        dreams = data.get('dreams')
        perspiration = data.get('perspiration')
        thermal_reaction = data.get('thermal_reaction')
        habits = data.get('habits')
        sexual_history = data.get('sexual_history')
        # menstrual / obstetric
        menarche_age = data.get('menarche_age')
        cycle = data.get('cycle')
        flow = data.get('flow')
        menopause = data.get('menopause')
        obstetric_history = data.get('obstetric_history')
        gravida = data.get('gravida')
        para = data.get('para')
        abortions = data.get('abortions')
        full_term_deliveries = data.get('full_term_deliveries')
        # mental generals
        mental_generals = data.get('mental_generals')
        # general physical
        built = data.get('built')
        height = data.get('height')
        weight = data.get('weight')
        pulse = data.get('pulse')
        bp = data.get('bp')
        temperature = data.get('temperature')
        respiration = data.get('respiration')
        pallor_cyanosis_edema = data.get('pallor_cyanosis_edema')
        tongue_nails_skin = data.get('tongue_nails_skin')
        # systemic
        respiratory_system = data.get('respiratory_system')
        cardiovascular_system = data.get('cardiovascular_system')
        gastrointestinal_system = data.get('gastrointestinal_system')
        genitourinary_system = data.get('genitourinary_system')
        nervous_system = data.get('nervous_system')
        locomotor_system = data.get('locomotor_system')
        # diagnosis/prescription
        allopathic_diagnosis = data.get('allopathic_diagnosis')
        miasmatic_diagnosis = data.get('miasmatic_diagnosis')
        totality_of_symptoms = data.get('totality_of_symptoms')
        repertorization = data.get('repertorization')
        chosen_remedy = data.get('chosen_remedy')
        potency = data.get('potency')
        repetition = data.get('repetition')
        basis_of_prescription = data.get('basis_of_prescription')
        receipe_image = request.FILES.get('receipe_image')
        # create Receipe instance and then write a case sheet file
        receipe = Receipe.objects.create(
            case_number = case_number,
            receipe_name = receipe_name,
            receipe_description = receipe_description,
            receipe_image = receipe_image,
            relation = relation,
            gender = gender,
            status = status,
            phone = phone,
            religion = religion,
            occupation = occupation,
            address = address,
            medical_history = medical_history,
            family_history = family_history,
            investigation = investigation
            ,age = age if age else None
            ,date = date if date else None
            ,appetite = appetite
            ,thirst = thirst
            ,cravings = cravings
            ,aversions = aversions
            ,bowel_habits = bowel_habits
            ,urine = urine
            ,sleep = sleep_field
            ,dreams = dreams
            ,perspiration = perspiration
            ,thermal_reaction = thermal_reaction
            ,habits = habits
            ,sexual_history = sexual_history
            ,menarche_age = menarche_age
            ,cycle = cycle
            ,flow = flow
            ,menopause = menopause
            ,obstetric_history = obstetric_history
            ,gravida = gravida
            ,para = para
            ,abortions = abortions
            ,full_term_deliveries = full_term_deliveries
            ,mental_generals = mental_generals
            ,built = built
            ,height = height
            ,weight = weight
            ,pulse = pulse
            ,bp = bp
            ,temperature = temperature
            ,respiration = respiration
            ,pallor_cyanosis_edema = pallor_cyanosis_edema
            ,tongue_nails_skin = tongue_nails_skin
            ,respiratory_system = respiratory_system
            ,cardiovascular_system = cardiovascular_system
            ,gastrointestinal_system = gastrointestinal_system
            ,genitourinary_system = genitourinary_system
            ,nervous_system = nervous_system
            ,locomotor_system = locomotor_system
            ,allopathic_diagnosis = allopathic_diagnosis
            ,miasmatic_diagnosis = miasmatic_diagnosis
            ,totality_of_symptoms = totality_of_symptoms
            ,repertorization = repertorization
            ,chosen_remedy = chosen_remedy
            ,potency = potency
            ,repetition = repetition
            ,basis_of_prescription = basis_of_prescription
            ,follow_up_date = follow_up_date if follow_up_date else None
        )

        # write a case sheet PDF for this receipe
        try:
            _write_case_pdf(receipe)
        except Exception as e:
            # don't block the request on file errors, but log to console
            print('Error writing case sheet PDF:', e)

        return redirect('/receipes/')
    
    queryset = Receipe.objects.all()

    # listing page no longer performs search or case sheet file lookup; that is handled by `search_patient`

    context = {"receipes": queryset}

    return render(request, "home/receipes.html", context)

def update_receipe(request, id):
    queryset = Receipe.objects.get(id=id)
    context = {"receipe": queryset}

    if request.method == "POST":
        data = request.POST
        print(data)

        # preserve old identifying info to handle file rename/remove if needed
        old_name = queryset.receipe_name
        old_case = queryset.case_number

        # extract form fields
        case_number = data.get('case_number')
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        age = data.get('age')
        date = data.get('date')
        follow_up_date = data.get('follow_up_date')
        # normalize date inputs
        try:
            if date:
                date = datetime.strptime(date, '%Y-%m-%d').date()
        except Exception:
            pass
        try:
            if follow_up_date:
                follow_up_date = datetime.strptime(follow_up_date, '%Y-%m-%d').date()
        except Exception:
            pass
        relation = data.get('relation')
        gender = data.get('gender')
        status = data.get('status')
        phone = data.get('phone')
        religion = data.get('religion')
        occupation = data.get('occupation')
        address = data.get('address')
        medical_history = data.get('medical_history')
        family_history = data.get('family_history')
        investigation = data.get('investigation')
        # personal history
        appetite = data.get('appetite')
        thirst = data.get('thirst')
        cravings = data.get('cravings')
        aversions = data.get('aversions')
        bowel_habits = data.get('bowel_habits')
        urine = data.get('urine')
        sleep_field = data.get('sleep')
        dreams = data.get('dreams')
        perspiration = data.get('perspiration')
        thermal_reaction = data.get('thermal_reaction')
        habits = data.get('habits')
        sexual_history = data.get('sexual_history')
        # menstrual / obstetric
        menarche_age = data.get('menarche_age')
        cycle = data.get('cycle')
        flow = data.get('flow')
        menopause = data.get('menopause')
        obstetric_history = data.get('obstetric_history')
        gravida = data.get('gravida')
        para = data.get('para')
        abortions = data.get('abortions')
        full_term_deliveries = data.get('full_term_deliveries')
        # mental generals
        mental_generals = data.get('mental_generals')
        # general physical
        built = data.get('built')
        height = data.get('height')
        weight = data.get('weight')
        pulse = data.get('pulse')
        bp = data.get('bp')
        temperature = data.get('temperature')
        respiration = data.get('respiration')
        pallor_cyanosis_edema = data.get('pallor_cyanosis_edema')
        tongue_nails_skin = data.get('tongue_nails_skin')
        # systemic
        respiratory_system = data.get('respiratory_system')
        cardiovascular_system = data.get('cardiovascular_system')
        gastrointestinal_system = data.get('gastrointestinal_system')
        genitourinary_system = data.get('genitourinary_system')
        nervous_system = data.get('nervous_system')
        locomotor_system = data.get('locomotor_system')
        # diagnosis/prescription
        allopathic_diagnosis = data.get('allopathic_diagnosis')
        miasmatic_diagnosis = data.get('miasmatic_diagnosis')
        totality_of_symptoms = data.get('totality_of_symptoms')
        repertorization = data.get('repertorization')
        chosen_remedy = data.get('chosen_remedy')
        potency = data.get('potency')
        repetition = data.get('repetition')
        basis_of_prescription = data.get('basis_of_prescription')
        receipe_image = request.FILES.get('receipe_image')

        # assign values to the instance
        queryset.case_number = case_number
        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description
        # safe cast age
        try:
            queryset.age = int(age) if age not in (None, '') else None
        except Exception:
            queryset.age = None
        queryset.date = date if date else None
        queryset.relation = relation
        queryset.gender = gender
        queryset.status = status
        queryset.phone = phone
        queryset.religion = religion
        queryset.occupation = occupation
        queryset.address = address
        queryset.medical_history = medical_history
        queryset.family_history = family_history
        queryset.investigation = investigation
        queryset.appetite = appetite
        queryset.thirst = thirst
        queryset.cravings = cravings
        queryset.aversions = aversions
        queryset.bowel_habits = bowel_habits
        queryset.urine = urine
        queryset.sleep = sleep_field
        queryset.dreams = dreams
        queryset.perspiration = perspiration
        queryset.thermal_reaction = thermal_reaction
        queryset.habits = habits
        queryset.sexual_history = sexual_history
        queryset.menarche_age = menarche_age
        queryset.cycle = cycle
        queryset.flow = flow
        queryset.menopause = menopause
        queryset.obstetric_history = obstetric_history
        queryset.gravida = gravida
        queryset.para = para
        queryset.abortions = abortions
        queryset.full_term_deliveries = full_term_deliveries
        queryset.mental_generals = mental_generals
        queryset.built = built
        queryset.height = height
        queryset.weight = weight
        queryset.pulse = pulse
        queryset.bp = bp
        queryset.temperature = temperature
        queryset.respiration = respiration
        queryset.pallor_cyanosis_edema = pallor_cyanosis_edema
        queryset.tongue_nails_skin = tongue_nails_skin
        queryset.respiratory_system = respiratory_system
        queryset.cardiovascular_system = cardiovascular_system
        queryset.gastrointestinal_system = gastrointestinal_system
        queryset.genitourinary_system = genitourinary_system
        queryset.nervous_system = nervous_system
        queryset.locomotor_system = locomotor_system
        queryset.allopathic_diagnosis = allopathic_diagnosis
        queryset.miasmatic_diagnosis = miasmatic_diagnosis
        queryset.totality_of_symptoms = totality_of_symptoms
        queryset.repertorization = repertorization
        queryset.chosen_remedy = chosen_remedy
        queryset.potency = potency
        queryset.repetition = repetition
        queryset.basis_of_prescription = basis_of_prescription

        # follow up date
        queryset.follow_up_date = follow_up_date if follow_up_date else (data.get('follow_up_date') if data.get('follow_up_date') else None)

        if receipe_image:
            queryset.receipe_image = receipe_image

        # save within try/except so errors are surfaced to the user via messages
        try:
            queryset.save()
            # ensure we have up-to-date values from DB
            queryset.refresh_from_db()
            print(f"Updated Receipe id={queryset.id} name={queryset.receipe_name} case={queryset.case_number}")
            messages.info(request, f"Saved: {queryset.receipe_name} ({queryset.case_number})")
        except Exception as e:
            print('Save error:', e)
            messages.error(request, f"Error saving record: {e}")
            # if AJAX, return JSON error
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            return render(request, "home/update_receipes.html", context)

        # update the case sheet file: remove old file if name/case changed
        try:
            media_root = getattr(settings, 'MEDIA_ROOT', None)
            if not media_root:
                media_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'media')

            def _name_to_path(name, case):
                base = slugify(name) if name else 'unknown'
                if case:
                    fname = f"{base}_{slugify(case)}.pdf"
                else:
                    fname = f"{base}.pdf"
                return os.path.join(media_root, 'case_sheets', fname)

            # write new PDF for the updated instance and remove old pdf if changed
            _write_case_pdf(queryset)
            _remove_old_case_file(old_name, old_case)
        except Exception as e:
            # don't block the flow on file errors, but surface a notice
            print('Error updating case sheet file:', e)
            messages.warning(request, f"Record saved, but case-sheet file update failed: {e}")
            # if AJAX, include warning in JSON
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({'status': 'ok', 'message': f'Record saved but case-sheet update failed: {e}'})

        messages.success(request, "Record updated successfully.")

        # determine AJAX reliably
        is_ajax = (request.headers.get('x-requested-with') == 'XMLHttpRequest') or (request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest')
        print('update_receipe is_ajax=', is_ajax)
        print('after save:', {'id': queryset.id, 'name': queryset.receipe_name, 'case': queryset.case_number})

        # If this is an AJAX request, return JSON (for inline toasts)
        if is_ajax:
            return JsonResponse({
                'status': 'ok',
                'message': 'Record updated successfully',
                'id': queryset.id
            })

        # For non-AJAX, follow PRG pattern: redirect to the same page so browser performs a GET
        return redirect(request.path)

    response = render(request, "home/update_receipes.html", context)
    # prevent browser caching of the edit page so users always see fresh data
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@login_required(login_url="/login/")
def delete_receipe(request, id):
    queryset = Receipe.objects.get(id = id)
    queryset.delete()
    messages.success(request, "Record deleted successfully.")
    # try to return user to referring page (search or listing); fall back to receipes
    redirect_to = request.META.get('HTTP_REFERER', '/receipes/')
    return redirect(redirect_to)

@login_required(login_url="/login/")
def search_patient(request):
    queryset = Receipe.objects.all()
    if request.GET.get('search'):
        q = request.GET.get('search')
        queryset = queryset.filter(
            Q(receipe_name__icontains=q) | Q(case_number__icontains=q)
        )

    # attach case_sheet_url attribute to each receipe if file exists (so template can show "Stored")
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if not media_root:
        media_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'media')

    def _find_case_file(receipe):
        name_slug = slugify(receipe.receipe_name) if receipe.receipe_name else 'unknown'
        case_slug = slugify(receipe.case_number) if receipe.case_number else None
        folder = os.path.join(media_root, 'case_sheets')
        if case_slug:
            fname = f"{name_slug}_{case_slug}.pdf"
            path = os.path.join(folder, fname)
            if os.path.exists(path):
                media_url = getattr(settings, 'MEDIA_URL', '/media/')
                return os.path.join(media_url, 'case_sheets', fname)
        if os.path.exists(folder):
            for f in os.listdir(folder):
                if f.startswith(name_slug + '_') and f.endswith('.pdf'):
                    media_url = getattr(settings, 'MEDIA_URL', '/media/')
                    return os.path.join(media_url, 'case_sheets', f)
        return None

    for r in queryset:
        try:
            r.case_sheet_url = _find_case_file(r)
        except Exception:
            r.case_sheet_url = None

    context = {"receipes":queryset}

    response = render(request, "home/search.html", context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response
 

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists(): #this is to check if username already exists
            messages.error(request,"Invalid username")
            return redirect('/login')
        
        user = authenticate(username=username, password = password)

        if user is None:
            messages.error(request,"Invalid password")
            return redirect('/login')
        else:
            login(request, user)
            return redirect('/receipes/')
        
    return render(request, "home/login.html")

@login_required(login_url="/login/")
def logout_page(request):
    logout(request)
    return redirect('/login')

def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        

        user = User.objects.filter(username=username) #this is to check if username already exists

        if user.exists():
            messages.info(request, "Username already taken") # Message if username exist
            return redirect('/register/')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username

        )

        user.set_password(password) #this is for password encryption as the password will be returned as a text.
        user.save()

        messages.info(request, "Account created successfully") # Message if user got created successfully

        return redirect('/login/')


    return render(request, "home/register.html")


# download_case_sheet removed — PDFs are stored in media/case_sheets/ but not served via view

    
