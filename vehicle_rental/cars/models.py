from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=255)
    category_image = models.ImageField(upload_to='static/images/website_photos', blank=True, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name


class Class(models.Model):
    class_name = models.CharField(max_length=255)
    class_image = models.ImageField(upload_to='static/images/website_photos', blank=True, null=True)

    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __str__(self):
        return self.class_name


class Car(models.Model):
    car_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    car_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    brand = models.CharField(max_length=127)
    model = models.CharField(max_length=127)
    manufacture_date = models.DateField()
    description = models.TextField(max_length=255)
    seats = models.IntegerField()
    doors = models.IntegerField()
    suitcases = models.IntegerField()

    TRANSMISSIONS = [
        ('AT', 'Automatic'),
        ('MN', 'Manual'),
    ]
    transmission = models.CharField(choices=TRANSMISSIONS, max_length=3)
    air_conditioner = models.BooleanField(default=True)
    min_driver_age = models.IntegerField(default=18)
    car_exterior_photo = models.ImageField(upload_to='static/images/car_photos')
    car_interior_photo = models.ImageField(upload_to='static/images/car_photos')

    availability = models.BooleanField(default=True)
    guarantee = models.BooleanField(default=False)
    discount = models.IntegerField(default=0)
    price = models.FloatField()
    deposit = models.FloatField(blank=True, null=True)
    location = models.CharField(max_length=127)

    car_booked_from = models.DateField()
    car_booked_to = models.DateField()

    long_distance_price = models.FloatField()
    per_km_price = models.FloatField()

    def __str__(self):
        return str(self.brand) + str(self.model)

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'

