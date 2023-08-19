from django.contrib import admin
from .models import CarMake, CarModel

# Register CarMake model with the admin site
@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

# Create an inline class for CarModel within CarMake admin page
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1

# Register CarModel model with the admin site
@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'dealer_id', 'car_type', 'year')

# Register CarMakeAdmin with the inline CarModelAdmin
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

# Re-register the CarMakeAdmin with inline
admin.site.unregister(CarMake)
admin.site.register(CarMake, CarMakeAdmin)
