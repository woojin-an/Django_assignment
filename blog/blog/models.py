from django.db import models

class Blog(models.Model):
    CATEGORY_CHOICES = (
        ('free', '자유'),
        ('travel', '여행'),
        ('food', '음식'),
        ('game', '게임'),
    )
    category = models.CharField('카테고리', max_length=15, choices=CATEGORY_CHOICES)
    title = models.CharField('제목', max_length=100)
    content = models.TextField('본문')
    # 작성자는 패스 (추후 업데이트)
    created_at = models.DateTimeField('작성일자', auto_now_add=True)
    updated_at = models.DateTimeField('작성일자', auto_now=True)

    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}'

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'
# 제목
# 본문
# 작성자
# 작성일자
# 수정일자
# 카테고리
