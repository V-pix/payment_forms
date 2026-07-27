from django.db import models


class Item(models.Model):
    name: str = models.CharField(
        max_length=200,
        verbose_name="Название товара",
        help_text="Укажите название товара",
    )
    description: str = models.TextField(
        verbose_name="Текстовое описание",
        help_text="Введите текстовое описание",
    )
    price: int = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена товара",
        help_text="Укажите цену товара",
        default=0,
    )
    
    class Meta:
        db_table = "items"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self) -> str:
        return self.name

