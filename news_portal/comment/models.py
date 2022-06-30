from django.conf import settings
from django.db import models

# Модель Comment
# Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.
# Модель будет иметь следующие поля:
# связь «один ко многим» с моделью Post;
# связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор);
# текст комментария;
# дата и время создания комментария;
# рейтинг комментария.


class Comment(models.Model):
    """Модель Комментария."""
    post = models.ForeignKey("post.Post", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField(null=False, blank=False, default=0)

    def like(self):
        """Увеличивает рейтинг на 1."""
        self.rating += 1
        self.save()

    def dislike(self):
        """Уменьшает рейтинг на 1."""
        if self.rating > 0:
            self.rating -= 1
            self.save()
