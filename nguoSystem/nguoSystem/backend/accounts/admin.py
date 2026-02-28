from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('email', 'full_name', 'phone', 'is_staff', 'is_approved', 'is_active', 'date_joined')
	list_filter = ('is_staff', 'is_approved', 'is_active', 'gender', 'tailor_type')
	search_fields = ('email', 'full_name', 'phone')
	readonly_fields = ('date_joined',)
	actions = ['approve_tailors', 'disapprove_tailors']
	
	fieldsets = (
		('Taarifa za Msingi', {
			'fields': ('email', 'full_name', 'phone', 'address', 'gender')
		}),
		('Profile', {
			'fields': ('bio', 'profile_picture')
		}),
		('Haki za Mshonaji', {
			'fields': ('is_staff', 'is_approved', 'tailor_type'),
			'description': 'is_staff = Mshonaji, is_approved = Amekubaliwa na admin'
		}),
		('Permissions', {
			'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions')
		}),
		('Tarehe', {
			'fields': ('date_joined', 'last_login')
		}),
	)

	def approve_tailors(self, request, queryset):
		"""Kubali washonaji waliosubiri"""
		updated = queryset.filter(is_staff=True, is_approved=False).update(is_approved=True)
		self.message_user(request, f'Washonaji {updated} wamekubaliwa!')

	def disapprove_tailors(self, request, queryset):
		"""Ondoa haki za washonaji"""
		updated = queryset.filter(is_staff=True).update(is_approved=False)
		self.message_user(request, f'Washonaji {updated} wamekataliwa!')

	approve_tailors.short_description = "✅ Kubali washonaji"
	disapprove_tailors.short_description = "❌ Kataa washonaji"
