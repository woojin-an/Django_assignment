from django.db import models

# models.py 는 DB의 테이블
# Field 는 DB의 컬럼

# 북마크
# 이름
# URL 주소


class Bookmark(models.Model):
    name = models.CharField('이름', max_length=100)
    url = models.URLField('URL')
    created_at = models.DateTimeField('생성일시', auto_now_add=True)
    updated_at = models.DateTimeField('수정일시', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '북마크'
        verbose_name_plural = '북마크 목록'

