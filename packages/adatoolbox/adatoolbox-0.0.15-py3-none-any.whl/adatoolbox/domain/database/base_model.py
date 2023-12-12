from django.db import models


class BaseModel(models.Model):
    establishment_id = models.CharField(
        "Estabelecimento",
        max_length=20,
        null=True)
    active = models.BooleanField(
        default=True)
    created_by = models.CharField(
        "Usuario criacao",
        max_length=50,
        null=True)
    updated_by = models.CharField(
        "Usuario edicao",
        max_length=50,
        null=True)
    deleted_by = models.CharField(
        "Usuario delecao",
        max_length=50,
        null=True)
    created_at = models.DateTimeField(
        "Criado em",
        auto_now_add=True)
    updated_at = models.DateTimeField(
        "Atualizado em",
        auto_now=True)
    deleted_at = models.DateTimeField(
        "Deletado em",
        null=True)
    
    class Meta:
        abstract = True

