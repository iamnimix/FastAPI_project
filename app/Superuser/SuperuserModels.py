from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
import sys
from .Schema import ModifyContent

sys.path.append("..")
from app.Core.dependencies import *
from app.Core.models import *
from app.Auth.AuthModels import get_user_from_cookie

BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH / "Templates"))
router = APIRouter(prefix="/superuser")


@router.get("/dashboard", response_class=HTMLResponse)
async def superuser_dashboard(request: Request, db=Depends(get_db), user=Depends(get_user_from_cookie)):
    if user["usertype"] == "superuser":
        messages = db.query(message).all()
        comments = db.query(Comment).all()
        posts = db.query(Post).all()
        users = db.query(User).filter(User.is_superuser == False).all()
        return templates.TemplateResponse("Superuser_dashboard.html",
                                          {"request": request, "messages": messages, "comments": comments,
                                           "posts": posts, "users": users})
    else:
        return templates.TemplateResponse("error-403/dist/index.html", {"request": request})


@router.delete("/messages")
async def delete_a_message(message_id: ModifyContent, db=Depends(get_db)) -> None:
    db_delete_message = db.query(message).filter(message.id == message_id.id).first()
    db.delete(db_delete_message)
    db.commit()


@router.delete("/comments")
async def delete_a_message(comment_id: ModifyContent, db=Depends(get_db)) -> None:
    db_delete_comment = db.query(Comment).filter(Comment.id == comment_id.id).first()
    db.delete(db_delete_comment)
    db.commit()


@router.patch("/comments")
async def approve_a_message(comment_id: ModifyContent, db=Depends(get_db)) -> None:
    db_comment = db.query(Comment).filter(Comment.id == comment_id.id).first()
    db_comment.confirmed = True
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)


@router.delete("/posts")
async def delete_a_post(post_id: ModifyContent, db=Depends(get_db)) -> None:
    db_delete_post = db.query(Post).filter(Post.id == post_id.id).first()
    db.delete(db_delete_post)
    db.commit()


@router.patch("/users")
async def change_a_user_access_level(user_id: ModifyContent, db=Depends(get_db)) -> None:
    db_user = db.query(User).filter(User.id == user_id.id).first()
    if db_user.is_admin is True:
        db_user.is_admin = False
    else:
        db_user.is_admin = True

    db.add(db_user)
    db.commit()
    db.refresh(db_user)


@router.delete("/users")
async def delete_a_user(user_id: ModifyContent, db=Depends(get_db)) -> None:
    db_delete_user = db.query(User).filter(User.id == user_id.id).first()
    db.delete(db_delete_user)
    db.commit()
