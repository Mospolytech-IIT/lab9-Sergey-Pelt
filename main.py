"""3. Веб-приложение"""
from fastapi import FastAPI, HTTPException, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from models import Base, User, Post

app = FastAPI()

templates = Jinja2Templates(directory="templates")

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/Labrab9"

engine = create_engine(DATABASE_URL)
new_session = sessionmaker(bind=engine)

def get_db():
    """Зависимость для подключения к базе данных"""
    db = new_session()
    try:
        Base.metadata.create_all(bind=engine)
        yield db
    finally:
        db.close()

@app.get("/users")
async def read_users(request: Request, db: Session = Depends(get_db)):
    """Маршрут для отображения списка пользователей и формы создания нового пользователя"""
    users = db.query(User).all()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.post("/users/create")
async def create_user(username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """Маршрут для сохранения нового пользователя"""
    new_user = User(username=username, email=email, password=password)
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/users", status_code=303)

@app.get("/users/edit/{user_id}")
async def edit_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    """Маршрут для отображения формы для редактирования пользователя"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("edit_user.html", {"request": request, "user": user})

@app.post("/users/edit/{user_id}")
async def update_user(user_id: int, username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """Маршрут для сохранения редактирования пользователя"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = username
    user.email = email
    user.password = password
    db.commit()
    return RedirectResponse(url="/users", status_code=303)

@app.get("/users/delete/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Маршрут для удаления пользователя"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return RedirectResponse(url="/users", status_code=303)

@app.get("/posts")
async def read_posts(request: Request, db: Session = Depends(get_db)):
    """Маршрут для отображения списка постов и формы создания нового поста"""
    posts = db.query(Post).all()
    users = db.query(User).all()
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts, "users": users})

@app.post("/posts/create")
async def create_post(title: str = Form(...), content: str = Form(...), user_id: int = Form(...), db: Session = Depends(get_db)):
    """Маршрут для сохранения нового поста"""
    new_post = Post(title=title, content=content, user_id=user_id)
    db.add(new_post)
    db.commit()
    return RedirectResponse(url="/posts", status_code=303)

@app.get("/posts/edit/{post_id}")
async def edit_post(post_id: int, request: Request, db: Session = Depends(get_db)):
    """Маршрут для отображения формы для редактирования поста"""
    post = db.query(Post).filter(Post.id == post_id).first()
    users = db.query(User).all()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("edit_post.html", {"request": request, "post": post, "users": users})

@app.post("/posts/edit/{post_id}")
async def update_post(post_id: int, title: str = Form(...), content: str = Form(...), user_id: int = Form(...), db: Session = Depends(get_db)):
    """Маршрут для сохранения редактирования поста"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.title = title
    post.content = content
    post.user_id = user_id
    db.commit()
    return RedirectResponse(url="/posts", status_code=303)

@app.get("/posts/delete/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Маршрут для удаления поста"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return RedirectResponse(url="/posts", status_code=303)
