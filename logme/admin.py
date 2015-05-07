from django.contrib import admin
from logme.models import Account, History
from django.contrib.auth.models import User


class HistoryInline(admin.TabularInline):
	readonly_fields = ['timein', 'timeout', 'totaltime']
	
	model = History

class AccountAdmin(admin.ModelAdmin):

	list_display = ['classtype', 'user','fullname']
	inlines = [HistoryInline]
	

admin.site.register(Account, AccountAdmin)

