from django.contrib import admin
from .models import CustomUser, Kuliner, Penginapan, Wisata
from django.core.exceptions import PermissionDenied

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role',)
    search_fields = ('username', 'email')

    def save_model(self, request, obj, form, change):
        """
        Logika untuk menyimpan CustomUser:
        - Hanya super_admin yang dapat membuat atau memperbarui pengguna dengan role admin atau super_admin.
        - is_staff dan is_superuser diatur otomatis berdasarkan role.
        """
        if not change:  # Jika objek baru
            if obj.role in ['admin', 'super_admin'] and request.user.role != 'super_admin':
                raise PermissionDenied("Hanya Super Admin yang dapat membuat Admin atau Super Admin.")
        else:  # Jika mengedit pengguna
            original_user = CustomUser.objects.get(pk=obj.pk)
            if original_user.role != obj.role and obj.role in ['admin', 'super_admin']:
                if request.user.role != 'super_admin':
                    raise PermissionDenied("Hanya Super Admin yang dapat mengubah role menjadi Admin atau Super Admin.")

        # Atur is_staff dan is_superuser otomatis berdasarkan role
        obj.is_staff = obj.role in ['admin', 'super_admin']
        obj.is_superuser = obj.role in ['super_admin', 'admin']

        # Hash password jika pengguna baru atau password diubah
        if not obj.pk or 'password' in form.changed_data:
            obj.set_password(obj.password)

        super().save_model(request, obj, form, change)

    def has_view_permission(self, request, obj=None):
        # Super_admin dapat melihat semua data, admin hanya data terkait selain pengguna
        return request.user.role in ['super_admin']

    def has_change_permission(self, request, obj=None):
        # Hanya super_admin yang dapat mengubah pengguna
        return request.user.role == 'super_admin'

    def has_add_permission(self, request):
        # Hanya super_admin yang dapat menambah pengguna
        return request.user.role == 'super_admin'

    def has_delete_permission(self, request, obj=None):
        # Hanya super_admin yang dapat menghapus pengguna
        return request.user.role == 'super_admin'

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Kuliner)
admin.site.register(Penginapan)
admin.site.register(Wisata)
