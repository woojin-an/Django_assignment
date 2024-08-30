from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from PIL import Image
from pathlib import Path
from io import BytesIO

User = get_user_model()


class Todo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_image = models.ImageField(verbose_name='이미지', null=True, blank=True, upload_to='todo/')
    thumbnail = models.ImageField(
        verbose_name='썸네일', null=True, blank=True,
        upload_to='todo/thumbnail', default='todo/no_image/NO-IMAGE.jpg'
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.completed_image:
            return super().save(*args, **kwargs)

        completed_image = Image.open(self.completed_image)
        completed_image.thumbnail((300, 300))

        image_path = Path(self.completed_image.name)

        thumbnail_name = image_path.stem # 이름 추출
        thumbnail_extension = image_path.suffix.lower() # 확장자 추출
        thumbnail_filename = f'{thumbnail_name}_thumb{thumbnail_extension}' # 썸네일 파일 이름 만들기

    # 썸네일 확장자별로 할당 매겨주기
        if thumbnail_extension in ['.jpg', '.jpeg']:
            file_type = 'JPEG'
        elif thumbnail_extension == '.gif':
            file_type = 'GIF'
        elif thumbnail_extension == '.png':
            file_type = 'PNG'
        else:
            return super().save(*args, **kwargs)

        temp_thumb = BytesIO()
        completed_image.save(temp_thumb, file_type)
        temp_thumb.seek(0)

        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)
        temp_thumb.close()
        return super().save(*args, **kwargs)

    def get_thumbnail_image_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.completed_image:
            return self.completed_image.url
        return None


class Comment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}: {self.message}'