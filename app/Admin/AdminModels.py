from fastapi import APIRouter, Request, Depends, File, UploadFile, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import date
from pathlib import Path
from .Schema import NewPost, PostID
import sys

sys.path.append("..")
from app.Core.dependencies import *
from app.Core.models import *
from app.Auth.AuthModels import get_user_from_cookie
# pip install python-multipart.
from starlette import status

BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH / "Templates"))
router = APIRouter(prefix="/admin")


@router.get("/dashboard")
async def all_posts(request: Request, db=Depends(get_db), user=Depends(get_user_from_cookie)):
    if user["usertype"] != "normal" and user["usertype"] != "not_logged_in":
        usr = db.query(User).filter(User.username == user["username"]).first()
        allposts = db.query(Post).filter(Post.owner_id == usr.id).order_by(Post.create_date.desc()).all()
        return templates.TemplateResponse("Admin_dashboard.html", {"request": request, "allposts": allposts})
    else:
        return templates.TemplateResponse("error-403/dist/index.html", {"request": request})


@router.post("/dashboard")
async def create_a_new_post(file: UploadFile, title=Form(), body=Form(), db=Depends(get_db),
                            user=Depends(get_user_from_cookie)):
    usr = db.query(User).filter(User.username == user["username"]).first()
    with open(f"static/{file.filename}", "wb") as f:
        f.write(file.file.read())
    post_date = date.today()
    post = Post(title=title, body=body, image=f"static/{file.filename}",
                create_date=post_date, owner=usr)
    db.add(post)
    db.commit()
    return "success"


@router.delete("/dashboard")
async def delete_a_post(post_id: PostID, db=Depends(get_db)):
    db_delete_post = db.query(Post).filter(Post.id == post_id.post_id).first()
    db.delete(db_delete_post)
    db.commit()
    return "success"
