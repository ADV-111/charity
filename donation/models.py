from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Institution(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=3,
                            choices=[
                                ('F', 'Fundacja'),
                                ('OP', 'Organizacja Pozarządowa'),
                                ('ZL', 'Zbiórka Lokalna')],
                            default='F')
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField(verbose_name='liczba worków')
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=1024)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        category_list = ', '.join(str(cat) for cat in self.categories.all())
        return f'{self.quantity} worków darów w postaci: {category_list}'



