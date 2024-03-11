from django.db import models
from users.models import User


class Collect(models.Model):

    BIRTHDAY = 'birthday'
    WEDDING = 'wedding'
    FUNERAL = 'funeral'
    REASONS = [
        (BIRTHDAY, 'День рождения'),
        (WEDDING, 'Свадьба'),
        (FUNERAL, 'Похороны'),
    ]

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='collects',
        verbose_name='Инициатор сбора',
    )

    title = models.CharField(
        max_length=300,
        verbose_name='Название сбора',
    )
    
    reason = models.CharField(
        verbose_name='Повод',
        max_length=32,
        choices=REASONS,
    )

    description = models.TextField(
        verbose_name='Описание сбора',
        max_length=320,
    )

    total = models.PositiveIntegerField(
        verbose_name='Сумма для сбора',
        blank=True,
        null=True
    )

    image = models.ImageField(
        verbose_name='Картинка',
        help_text='Место для кратинки',
        upload_to='events/',
        blank=True
    )

    start = models.DateTimeField(
        verbose_name='Начало сбора',
        auto_now_add=True,
    )

    end = models.DateTimeField(
        verbose_name='Срок',
        help_text='гггг-мм-дд ч:м',
    )

    @property
    def duration(self):
        return self.end - self.start

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-end',)
        verbose_name = 'Сбор'
        verbose_name_plural = 'Сборы'


class Payment(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Донатер'
    )

    event = models.ForeignKey(
        Collect,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Событие'
    )

    amount = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Внесение денег'
        verbose_name_plural = 'Донаты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'event'],
                name='unique_event_donation'
            )
        ]
