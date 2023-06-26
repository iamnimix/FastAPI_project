from datetime import date

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.Core.models import *
from app.Core.dependencies import *
from pathlib import Path
from app.Auth.AuthModels import get_user_from_cookie
from .Schema import Comments

BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH / "Templates"))
router = APIRouter()


@router.get("/post/{id}", response_class=HTMLResponse)
async def detail_post(id, request: Request, db=Depends(get_db), user=Depends(get_user_from_cookie)):
    post = db.query(Post).filter(Post.id == id).first()
    comments = db.query(Comment.id, Comment.description, Comment.date_created, Comment.confirmed, Comment.post_id,
                        User.fullname).join(User, Comment.owner_id == User.id).filter(
        Comment.confirmed == True, Comment.post_id == id).order_by(Comment.date_created.desc()).all()
    print(post.view_count)
    post.view_count += 1
    db.add(post)
    db.commit()
    db.refresh(post)

    return templates.TemplateResponse("revolve/standard-fullwidth.html",
                                      {"request": request, "post": post,
                                       "comments": comments, "usertype": user["usertype"]})


@router.post("/post")
async def comment(user_comment: Comments, db=Depends(get_db), user=Depends(get_user_from_cookie)) -> None:
    """
    Create a comment for a post
    :param user: check Login condition first
    :param db: call database to store user comments
    :param user_comment: User Comment on a post that comes from front-end. Must check with pydantic model to validate.
    :return: None
    """
    user_requesting = db.query(User).filter(User.username == user["username"]).first()
    post = db.query(Post).filter(Post.id == user_comment.post_id).first()
    db_comment = Comment(description=user_comment.description, date_created=date.today(), owner=user_requesting,
                         on_post=post)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return


@router.get("/allposts/", response_class=HTMLResponse)
async def all_posts(request: Request, db=Depends(get_db), user=Depends(get_user_from_cookie)):
    usertype = user["usertype"]
    allposts = db.query(Post.id, Post.image, Post.title, Post.body, Post.create_date, Post.owner_id,
                        User.fullname).join(User, Post.owner_id == User.id).order_by(Post.create_date.desc()).all()
    return templates.TemplateResponse("Posts.html", {"request": request, "posts": allposts, "usertype": usertype})
