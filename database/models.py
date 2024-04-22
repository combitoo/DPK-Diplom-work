from tortoise import Model, fields


class User(Model):
    id = fields.IntField(pk=True)
    
    username = fields.CharField(max_length=32, default="Нет имени")
    hashed_password = fields.CharField(max_length=256)

    role = fields.CharField(max_length=128, default="user")
    description = fields.CharField(max_length=512, default="Привет! Это мой блог...")
    avatar_link = fields.CharField(max_length=1024)

    post_amount = fields.IntField()

    disabled = fields.BooleanField(default=False)
    is_admin = fields.BooleanField(default=False)


class Post(Model):
    id = fields.IntField(pk=True)

    title = fields.CharField(max_length=128)
    text = fields.CharField(max_length=10240)
    preview_link = fields.CharField(max_length=1024)
    created_by: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="users"
    )

    categories = fields.ManyToManyField("models.Category", related_name="posts")

    time_to_read = fields.CharField(max_length=256)

    post_rating = fields.IntField()

    created_at = fields.DatetimeField(auto_now_add=True)  # Когда был создан пост
    edited_at = fields.DatetimeField(auto_now=True)  # Когда был отредактирован


class Comment(Model):
    id = fields.IntField(pk=True)

    text = fields.CharField(max_length=256)
    created_by: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="comments"
    )
    post: fields.ForeignKeyRelation[Post] = fields.ForeignKeyField(
        "models.Post", related_name="posts"
    )

    created_at = fields.DatetimeField(auto_now_add=True)  # Когда был создан комментарий
    edited_at = fields.DatetimeField(auto_now=True)  # Когда был отредактирован


class Category(Model):
    id = fields.IntField(pk=True)

    name = fields.CharField(max_length=128)
    description = fields.CharField(max_length=512)

    post_amount = fields.IntField()

    created_at = fields.DatetimeField(auto_now_add=True)  # Когда был создана категория
    edited_at = fields.DatetimeField(auto_now=True)  # Когда была отредактирована категория