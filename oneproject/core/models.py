from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    cidade = models.CharField(max_length=100)
    descricao = models.TextField()
    celular = models.CharField(max_length=11)
    email = models.EmailField()
    postagem = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField()
    ativo = models.BooleanField(default=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'produtos'
