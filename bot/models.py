from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=20, verbose_name="ID пользователя")
    username = models.CharField(max_length=50, verbose_name='Username пользователя')
    
    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class DaylyWriting(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user"
    )
    writing = models.TextField(verbose_name="Записи за день", null=True, blank=True)
    day = models.DateField(verbose_name="Дата")

    def __str__(self):
        return str(self.day)

    class Meta:
        verbose_name = 'Запись за день'
        verbose_name_plural = 'Записи за день'