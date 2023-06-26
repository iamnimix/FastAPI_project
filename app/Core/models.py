from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from . import database


class User(database.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="owner")


class Post(database.Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String)  # keeps the url to the image
    title = Column(String, index=True)
    body = Column(String, index=True)
    create_date = Column(String)
    view_count = Column(Integer,default=0)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
    post_comments = relationship("Comment", back_populates="on_post")


class Comment(database.Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    date_created = Column(String)
    confirmed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

    owner = relationship("User", back_populates="comments")
    on_post = relationship("Post", back_populates="post_comments")


class message(database.Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    created_by = Column(String)
    date_created = Column(String)
    email = Column(String)
    description = Column(String)
    read = Column(Boolean, default=False)
