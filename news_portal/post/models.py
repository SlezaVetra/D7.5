from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import m2m_changed

from .tasks import send_new_post_notification

# Модель Category
# Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.).
# Имеет единственное поле: название категории. Поле должно быть уникальным (в определении поля необходимо написать параметр unique = True).


class Category(models.Model):
    """Модель Категрия постов."""
    name = models.CharField(null=False, blank=False, unique=True, max_length=100)
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, through="CategorySubscribers")


class CategorySubscribers(models.Model):
    """Модель для связи Пользователей-подписчиков на Категорию постов."""
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


POST_NEWS = 0
POST_POST = 1
POST_TYPE = (
    (POST_NEWS, "Новость"),
    (POST_POST, "Статья"),
)


# Модель PostCategory
# Промежуточная модель для связи «многие ко многим»:
# связь «один ко многим» с моделью Post;
# связь «один ко многим» с моделью Category.

class PostCategory(models.Model):
    """Модель-связка Постов с Категориями."""
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)


# Модель Post
# Эта модель должна содержать в себе статьи и новости, которые создают пользователи. Каждый объект может иметь одну или несколько категорий.
# Соответственно, модель должна включать следующие поля:
# связь «один ко многим» с моделью Author;
# поле с выбором — «статья» или «новость»;
# автоматически добавляемая дата и время создания;
# связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
# заголовок статьи/новости;
# текст статьи/новости;
# рейтинг статьи/новости.

class Post(models.Model):
    """Модель Поста."""
    author = models.ForeignKey("author.Author", on_delete=models.CASCADE, related_name="posts")
    post_type = models.PositiveSmallIntegerField(null=False, blank=False, choices=POST_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField("Category", through=PostCategory)
    title = models.CharField(null=False, blank=False, max_length=100)
    text = models.TextField(null=False, blank=False)
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

    def preview(self):
        """Возвращает первые 124 символа текста Поста."""
        return self.text[:124]


@receiver(m2m_changed, sender="post.PostCategory")
def new_post_notify(sender, **kwargs):
    """Отправляет оповещение о новом Посте подписчику Катеогрии."""
    instance = kwargs.get("instance")
    categories = kwargs.get("pk_set")
    send_new_post_notification.delay(instance.id, tuple(categories))
