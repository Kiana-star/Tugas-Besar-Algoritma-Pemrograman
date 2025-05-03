from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q
from .models import Kuliner, Penginapan, Wisata
from .forms import SignupForm, WisataForm, PenginapanForm, KulinerForm
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404

def pilih(request):
    return render(request, 'posting/pilih.html')

def kategori_view(request, kategori):
    return render(request, f'{kategori}.html')

def search_query(request, model_class):
    query = request.GET.get('q', '')
    if query:
        return model_class.objects.filter(
            Q(nama__icontains=query) | Q(deskripsi__icontains=query)
        )
    return model_class.objects.all()

def search_results(request):
    query = request.GET.get('q')
    penginapan = kuliner = wisata = None

    if query:
        penginapan = Penginapan.objects.filter(
            Q(nama__icontains=query) | Q(deskripsi__icontains=query)
        )
        kuliner = Kuliner.objects.filter(
            Q(nama__icontains=query) | Q(deskripsi__icontains=query)
        )
        wisata = Wisata.objects.filter(
            Q(nama__icontains=query) | Q(deskripsi__icontains=query)
        )

        print("Hasil pencarian penginapan:", penginapan)
        print("Hasil pencarian kuliner:", kuliner)
        print("Hasil pencarian wisata:", wisata)

    context = {
        'query': query,
        'penginapan': penginapan,
        'kuliner': kuliner,
        'wisata': wisata,
    }
    return render(request, 'posting/search_results.html', context)

def kuliner(request):
    kuliner_data = search_query(request, Kuliner)
    return render(request, 'posting/kuliner.html', {'kuliner': kuliner_data, 'query': request.GET.get('q', '')})

def wisata(request):
    wisata_data = search_query(request, Wisata)
    return render(request, 'posting/wisata.html', {'wisata': wisata_data, 'query': request.GET.get('q', '')})

def penginapan(request):
    penginapan_data = search_query(request, Penginapan)
    return render(request, 'posting/penginapan.html', {'penginapan': penginapan_data, 'query': request.GET.get('q', '')})

@login_required
def contributor_dashboard(request):
    if request.user.role != 'contributor':
        return HttpResponseForbidden("Anda tidak memiliki izin untuk mengakses halaman ini.")
    
    kuliner_count = Kuliner.objects.filter(created_by=request.user).count()
    penginapan_count = Penginapan.objects.filter(created_by=request.user).count()
    wisata_count = Wisata.objects.filter(created_by=request.user).count()
    
    return render(request, 'posting/contributor_dashboard.html', {
        'kuliner_count': kuliner_count,
        'penginapan_count': penginapan_count,
        'wisata_count': wisata_count,
    })

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'super_admin':
                return redirect('pilih')
            elif user.role == 'admin':
                return redirect('pilih')
            elif user.role == 'contributor':
                return redirect('contributor_dashboard')
            else:
                return redirect('index')
        else:
            messages.error(request, "Username atau password salah.")
    else:
        form = AuthenticationForm()
    return render(request, 'posting/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    messages.success(request, "Anda telah berhasil keluar.")
    return redirect('pilih')

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup berhasil! Selamat datang, Contributor!")
            return redirect('contributor_dashboard')
        else:
            messages.error(request, "Ada masalah dengan pendaftaran Anda. Periksa formulir Anda.")
    else:
        form = SignupForm()
    return render(request, 'posting/signup.html', {'form':form})

@login_required
def tambah(request, kategori):
    if not request.user.role in ['admin', 'super_admin', 'contributor']:
        return HttpResponseForbidden("Anda tidak memiliki izin untuk menambahkan tempat.")
    
    if request.method == 'POST':
        nama = request.POST.get('nama')
        deskripsi = request.POST.get('deskripsi')
        google_maps_url = request.POST.get('google_maps_url', '')
        foto = request.FILES.get('foto')
        
        model = {'kuliner': Kuliner, 'penginapan': Penginapan, 'wisata': Wisata}.get(kategori)
        
        if model:
            model.objects.create(
                nama=nama,
                deskripsi=deskripsi,
                google_maps_url=google_maps_url,
                foto=foto,
                created_by=request.user
            )
            return redirect(kategori)
    
    return render(request, 'posting/tambah.html', {'kategori': kategori})

def hapus_tempat(request, kategori, tempat_id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Anda harus login untuk menghapus tempat.")
    
    model = {'kuliner': Kuliner, 'penginapan': Penginapan, 'wisata': Wisata}.get(kategori)
    if model:
        tempat = get_object_or_404(model, id=tempat_id)
        if request.user.role in ['super_admin', 'admin'] or (request.user == tempat.created_by):
            tempat.delete()
            return redirect(kategori)
        else:
            return HttpResponseForbidden("Anda tidak memiliki izin untuk menghapus tempat ini.")

def credits(request):
    return render(request, 'posting/credits.html')

@login_required
def edit_tempat(request, kategori, tempat_id):
    if kategori == 'wisata':
        model = Wisata
        form_class = WisataForm
    elif kategori == 'penginapan':
        model = Penginapan
        form_class = PenginapanForm
    elif kategori == 'kuliner':
        model = Kuliner
        form_class = KulinerForm
    else:
        return redirect('')

    tempat = get_object_or_404(model, id=tempat_id)

    if request.user.role not in ['admin', 'super_admin'] and request.user != tempat.created_by:
        return HttpResponseForbidden("Anda tidak memiliki izin untuk mengedit tempat ini.")
    
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=tempat)
        if form.is_valid():

            form.save()
            return redirect(f'{kategori}')
        else:
            print(form.errors)
    else:
        form = form_class(instance=tempat)

    return render(request, 'posting/edit.html', {'form': form, 'tempat': tempat, 'kategori': kategori})