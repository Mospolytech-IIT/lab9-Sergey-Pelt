"""2. Функции"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Post

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/Labrab9"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def add_users():
    """Функция, добавляющая несолько пользователей"""
    users = [
        User(username="Иван", email="ivan@email.com", password="1234"),
        User(username="Игорь", email="igor@email.com", password="5678"),
        User(username="Антон", email="anton@email.com", password="9876")
    ]
    session.add_all(users)
    session.commit()
    print("Пользователи добавлены.")

def add_posts():
    """Функция, добавляющая несолько постов"""
    posts = [
        Post(title="Первый пост", content="Первый пост от первого пользователя.", user_id=1),
        Post(title="Второй пост", content="Второй пост от первого пользователя.", user_id=1),
        Post(title="Третий пост", content="Первый пост от второго пользователя.", user_id=2),
        Post(title="Четвёртый пост", content="Второй пост от второго пользователя.", user_id=2),
        Post(title="Пятый пост", content="Первый пост от третьего пользователя.", user_id=3),
        Post(title="Шестой пост", content="Второй пост от третьего пользователя.", user_id=3)
    ]
    session.add_all(posts)
    session.commit()
    print("Посты добавлены.")

def get_all_users():
    """Функция, выводящая список всех пользователей"""
    users = session.query(User).all()
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")


def get_all_posts_with_users():
    """Функция, выводящая список всех постов"""
    posts = session.query(Post).all()
    for post in posts:
        user = session.query(User).filter(User.id == post.user_id).first()
        print(f"Название: {post.title}, содержание: {post.content}, пользователь: {user.username}")

def get_posts_by_user(user_id):
    """Функция, выводящая все посты пользователя по его id"""
    posts = session.query(Post).filter(Post.user_id == user_id).all()
    for post in posts:
        print(f"Название: {post.title}, содержание: {post.content}")

def update_user_email(user_id, new_email):
    """Функция, обновляющая email пользователя"""
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.email = new_email
        session.commit()
        print(f"Email пользователя с ID {user_id} обновлён.")
    else:
        print(f"Пользователь с ID {user_id} не найден.")

def update_post_content(post_id, new_content):
    """Функция, обновляющая содержание поста"""
    post = session.query(Post).filter(Post.id == post_id).first()
    if post:
        post.content = new_content
        session.commit()
        print(f"Содержание поста с ID {post_id} обновлено.")
    else:
        print(f"Пост с ID {post_id} не найден.")

def delete_post(post_id):
    """Функция, удаляющая пост"""
    post = session.query(Post).filter(Post.id == post_id).first()
    if post:
        session.delete(post)
        session.commit()
        print(f"Пост с ID {post_id} удалён.")
    else:
        print(f"Пост с ID {post_id} не найден.")

def delete_user_and_posts(user_id):
    """Функция, удаляющая пользователя и все его посты"""
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        session.query(Post).filter(Post.user_id == user_id).delete()
        session.delete(user)
        session.commit()
        print(f"Пользователь с ID {user_id} и все его посты удалены.")
    else:
        print(f"Пользователь с ID {user_id} не найден.")
def run_all_functions():
    """Запускает все функции"""
    add_users()
    add_posts()
    get_all_users()
    get_all_posts_with_users()
    get_posts_by_user(2)
    update_user_email(1, "newemail@email.com")
    update_post_content(3, "Новое содержание для поста.")
    delete_post(2)
    delete_user_and_posts(3)
if __name__ == "__functions__":
    run_all_functions()
