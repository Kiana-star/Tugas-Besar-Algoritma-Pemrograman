from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from posting import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Halaman utama
    path('', views.pilih, name='pilih'),

    # Autentikasi
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),  # Login dengan view kustom
    path('logout/', auth_views.LogoutView.as_view(next_page='pilih'), name='logout'),

    # Dashboard contributor
    path('contributor_dashboard/', views.contributor_dashboard, name='contributor_dashboard'),
    path('tambah/<str:kategori>/', views.tambah, name='tambah'),

    # CRUD data tempat (Kuliner, Penginapan, Wisata)
    path('wisata/', views.wisata, name='wisata'),
    path('kuliner/', views.kuliner, name='kuliner'),
    path('penginapan/', views.penginapan, name='penginapan'),
    path('<str:kategori>/tambah/', views.tambah, name='tambah'),
    path('<str:kategori>/<int:tempat_id>/hapus/', views.hapus_tempat, name='hapus_tempat'),
    path('search/', views.search_results, name='search_results'),
    path('<str:kategori>/', views.kategori_view, name='kategori'),


    # Ubah role pengguna (khusus Super Admin)
    path('<str:kategori>/edit/<int:tempat_id>/', views.edit_tempat, name='edit'),
    path('credits/', views.credits, name='credits'),
]

# Konfigurasi untuk media file
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
