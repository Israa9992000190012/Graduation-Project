from django.db import models
from django.urls import reverse

class Material(models.Model):

    MATARIAL = (
        ('Cotton', 'Cotton'),
        ('Polyester', 'Polyester'),
        ('Silk', 'Silk'),
        ('Wool', 'Wool'),
        ('Leather', 'Leather'),
        ('Fur', 'Fur'),
        ('Linen', 'Linen'),
        ('Rayon', 'Rayon'),
    )

    material_name = models.CharField(max_length=100, choices=MATARIAL)

    def __str__(self):
        return self.material_name

    class Meta:
        verbose_name_plural = 'Materials'


# Create your models here.
class Product(models.Model):

    CATEGORY = (
        ('Fashion-Accessories', 'Fashion-Accessories'),
        ('men-s-clothing', 'men-s-clothing'),
        ('women-s-clothing', 'women-s-clothing'),
        ('Kids', 'Kids'),
        ('Home', 'Home'),
        ('Men-Black t-shirt', 'Men-Black t-shirt'),
        ('Men-White t-shirt', 'Men-White t-shirt'),
        ('Men-Blue t-shirt', 'Men-Blue t-shirt'),
        ('Men-Red t-shirt', 'Men-Red t-shirt'),
        ('Men-Green t-shirt', 'Men-Green t-shirt'),
        #------------------------
        ('Women-dress-white', 'Women-dress-white'),
        ('Women-dress-red', 'Women-dress-red'),
        ('Women-dress-blue', 'Women-dress-blue'),
        #------------------------
        ('Hat-black', 'Hat-black'),
        ('Hat-white', 'Hat-white'),
        ('Hat-blue', 'Hat-blue'),
        ('Hat-red', 'Hat-red'),
        ('Hat-green', 'Hat-green'),
        #------------------------
        ('Black-jeans', 'Black-jeans'),
        ('White-jeans', 'White-jeans'),
        #------------------------
        ('Black-shoes', 'Black-shoes'),
        ('White-shoes', 'White-shoes'),
        ('Blue-shoes', 'Blue-shoes'),
        ('Red-shoes', 'Red-shoes'),
        ('Green-shoes', 'Green-shoes'),
        #------------------------
        ('Black-sweater', 'Black-sweater'),
        ('White-sweater', 'White-sweater'),
        ('Blue-sweater', 'Blue-sweater'),
        ('Red-sweater', 'Red-sweater'),
        #------------------------
        ('Black-jacket', 'Black-jacket'),
        ('White-jacket', 'White-jacket'),
        ('Blue-jacket', 'Blue-jacket'),
        ('Red-jacket', 'Red-jacket'),

    )
    
    product_name = models.CharField(max_length=200)
    product_price = models.CharField(max_length=200, default=None)
    product_cat = models.CharField(max_length=100, choices=CATEGORY)
    quantity_available = models.IntegerField(default=0)
    product_material = models.ManyToManyField(Material, related_name='material')
    product_image = models.ImageField(upload_to='product_images', blank=True, null=True,)
    rate = models.IntegerField(default=0)


    def __str__(self):
        return self.product_name

    @property
    def imageURL(self):
        try:
            url = self.product_image
        except:
            url = ''
        return url
    
    
    def get_absolute_url(self):
        return reverse('product', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Products'

      
class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name_plural = 'Product Materials'

