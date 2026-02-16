from django.db.models import(
    CharField,
    TextField,
    ForeignKey,
    DateTimeField,
    SlugField,
    ManyToManyField,
    TextChoices,
    CASCADE,
    SET_NULL,
)

#PROJECT imports 
from apps.abstract.models import AbstractTimeStampModel
from apps.users.models import CustomUser 


CATEGORY_MAX_NAME_LENGTH = 100 
TAG_MAX_NAME_LENGTH = 50 
POST_TITLE_MAX_LENGTH = 200 


class Category(AbstractTimeStampModel):
    """
    Docstring for Category
    """
    name = CharField(
        max_length=CATEGORY_MAX_NAME_LENGTH,
        unique=True,
    )
    slug = SlugField(
        unique=True,
    )


class Tag(AbstractTimeStampModel):
    """
    Docstring for Tag
    """
    name = CharField(
        max_length=TAG_MAX_NAME_LENGTH,
        unique=True,
    )
    slug = SlugField(
        unique=True,

    )


class Post(AbstractTimeStampModel):
    """
    Docstring for Post
    """
    class Status(TextChoices):
        DRAFT = "draft"
        PUBLISHED = "published"

    
    author = ForeignKey(
        to=CustomUser, 
        on_delete= CASCADE, 
        related_name="posts",
    )

    title = CharField(
        max_length=POST_TITLE_MAX_LENGTH,
    )
    slug = SlugField(
        unique=True,
    )
    body = TextField()

    category = ForeignKey(
        to=Category,
        on_delete=SET_NULL,
        null=True,  
        blank=True, 
        related_name="posts",
    )
    tags = ManyToManyField(
        to=Tag,
        blank=True,
        related_name="posts",

    )

    status=CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )



class Comment(AbstractTimeStampModel):
    """
    Docstring for Comment
    """

    post=ForeignKey(
        to=Post,
        on_delete=CASCADE,
        related_name="comments",
    )
    author=ForeignKey(
        to=CustomUser,
        on_delete=CASCADE,
        related_name="comments",
    )
    body=TextField(
    )




    


    