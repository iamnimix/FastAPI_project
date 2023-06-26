from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from .Schema import Messages
from app.Core.models import *
from app.Core.dependencies import *
from app.Auth.AuthModels import get_user_from_cookie
from datetime import date

BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH / "Templates"))
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root(request: Request, db=Depends(get_db), user=Depends(get_user_from_cookie)):
    recent_posts = db.query(Post).order_by(
        Post.create_date.desc()).limit(8).all()

    most_visited_posts = db.query(Post).order_by(Post.view_count.desc()).limit(3).all()

    return templates.TemplateResponse("revolve/index.html",
                                      {"request": request, "posts": recent_posts,
                                       "most_visited_posts": most_visited_posts, "usertype": user["usertype"]})


@router.get("/contact-us", response_class=HTMLResponse)
async def contactus(request: Request, user=Depends(get_user_from_cookie)):
    return templates.TemplateResponse("revolve/contact.html", {"request": request, "usertype": user["usertype"]})


@router.post("/contact-us")
async def sendmessage(messages: Messages, db=Depends(get_db)) -> None:
    """
    Create a message for Superuser
    :param db: call database to store user messages
    :param messages: message of user that comes from front-end. Must check with pydantic model to validate.
    :return: None
    """
    db_message = message(created_by=messages.created_by, date_created=date.today(),
                         email=messages.email, description=messages.description)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return


@router.get("/about-us", response_class=HTMLResponse)
async def aboutus(request: Request, user=Depends(get_user_from_cookie)):
    return templates.TemplateResponse("revolve/about.html", {"request": request, "usertype": user["usertype"]})
