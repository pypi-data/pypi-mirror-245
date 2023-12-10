from django.db import models


class Province(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name_en = models.CharField(max_length=100, db_index=True)
    name_th = models.CharField(max_length=100, db_index=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return str(self.name_th)


class District(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='districts')
    name_en = models.CharField(max_length=100, db_index=True)
    name_th = models.CharField(max_length=100, db_index=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'{self.province.name_th} / {self.name_th}'


class Subdistrict(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='subdistricts')
    name_en = models.CharField(max_length=100, db_index=True)
    name_th = models.CharField(max_length=100, db_index=True)

    class Meta:
        ordering = ('id',)

    def get_province(self):
        return self.district.province

    def __str__(self):
        return f'{self.get_province().name_th} / {self.district.name_th} / {self.name_th}'
