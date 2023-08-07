from django.db import models


class Slider(models.Model):
    image = models.ImageField(upload_to='slider')
    title = models.CharField(max_length=150, null=True)
    subtitle = models.CharField(max_length=150, null=True)
    content = models.CharField(max_length=150, null=True)
    is_active =  models.BooleanField(default=False)


    def __str__(self) -> str:
        return f"{self.title}"
    


class About(models.Model):
    image = models.ImageField(upload_to='slider')
    title = models.CharField(max_length=150, null=True)
    subtitle = models.CharField(max_length=150, null=True)
    content = models.CharField(max_length=150, null=True)


    def __str__(self) -> str:
        return f"{self.title}"
    



class Courses(models.Model):
    image = models.ImageField(upload_to='slider')
    title = models.CharField(max_length=150, null=True)
    subtitle = models.CharField(max_length=150, null=True)
    content = models.CharField(max_length=150, null=True)


    def __str__(self) -> str:
        return f"{self.title}"
    


class Logo(models.Model):
    image = models.ImageField(upload_to='logo')

    def __str__(self) -> str:
        return f"Logo"