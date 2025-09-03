from django.contrib import admin
from .models import Receipe


@admin.register(Receipe)
class ReceipeAdmin(admin.ModelAdmin):
	list_display = ('case_number', 'receipe_name', 'phone', 'gender', 'status')
	search_fields = ('receipe_name', 'case_number', 'phone')
	list_filter = ('gender', 'status')
