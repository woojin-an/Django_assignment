from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


User = get_user_model()


class Blog(models.Model):
    CATEGORY_CHOICES = (
        ('free', '자유'),
        ('travel', '여행'),
        ('food', '음식'),
        ('game', '게임'),
    )
    category = models.CharField('카테고리', max_length=15, choices=CATEGORY_CHOICES, default='free')
    title = models.CharField('제목', max_length=100)
    content = models.TextField('본문')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # models.CASCAED --> 같이 삭제됨
    # models.PROTECT --> 삭제가 불가능함 (유저를 삭제하려고 할 때 블로그가 있으면 유저 삭제 불가능)
    # models.SET_NULL --> 유저 삭제 시 블로그의 author가 NULL이 됨 (뒤에 null=True 필요함)
    created_at = models.DateTimeField('작성일자', auto_now_add=True)
    updated_at = models.DateTimeField('작성일자', auto_now=True)

    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}'

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'
# 제목
# 본문
# 작성자
# 작성일자
# 수정일자
# 카테고리
