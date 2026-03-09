from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


db = SQLAlchemy()

class User(db.Model):
    __tablename__="user_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(
        String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(
        String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    
    #Seguidores que sigo
    following: Mapped[List["Follower"]]=relationship("Follower", foreign_keys="Follower.user_from_id", back_populates="follower_user")

    #Seguidores que me siguen
    followers: Mapped[List["Follower"]]=relationship("Follower", foreign_keys="Follower.user_to_id", back_populates="followed_user")

    #Posts
    posts: Mapped[List["Post"]] = relationship('Post', back_populates="author")

    #Comments
    comments:Mapped[List["Comment"]] = relationship('Comment', back_populates="author")

    def serialize(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Follower(db.Model):
     
    __tablename__="follower_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Seguidor
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    
    # Seguido
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))

    follower_user: Mapped["User"] = relationship("User", foreign_keys=[user_from_id], back_populates ="following")
    followed_user: Mapped["User"] = relationship("User", foreign_keys=[user_to_id], back_populates="followers")


class Post(db.Model):
     
    __tablename__= "post_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    
    author: Mapped["User"] = relationship(back_populates="posts")
    media: Mapped[List["Media"]] = relationship(back_populates="post")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")

class Media(db.Model):
    __tablename__= "media_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[enumerate] = mapped_column(String(50))
    url: Mapped[str] = mapped_column(String(300))
    
    post_id: Mapped[int] = mapped_column(ForeignKey("post_table.id"), nullable=False)
    post: Mapped["Post"] = relationship(back_populates="media")

class Comment(db.Model):
    __tablename__= "comment_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(500))
    
    author_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post_table.id"), nullable=False)
    
    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")