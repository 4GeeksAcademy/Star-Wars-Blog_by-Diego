from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from datetime import datetime, timezone


db = SQLAlchemy()

class User(db.Model):
    __tablename__="users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    profile: Mapped["UserProfile"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    fav_planets: Mapped[List["Fav_Planet"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    fav_characters: Mapped[List["Fav_Character"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "profile": self.profile.username if self.profile else None
            # do not serialize the password, its a security breach
        }


class UserProfile(db.Model):
    __tablename__="user_profiles"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(
        String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(
        String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="profile")  
    
    def serialize(self):
        return {
            "id": self.id,
            "fullname": f"{self.firstname} {self.lastname}",
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Planet(db.Model):
     
    __tablename__="planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500))
    
    residents: Mapped[List["Character"]] = relationship(back_populates="homeworld")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "residents": [res.name for res in self.residents]
        }
    

class Character(db.Model):
    __tablename__="characters"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(String(500))
    
    homeworld_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    homeworld: Mapped["Planet"] = relationship(back_populates="residents")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "bio": self.bio,
            "homeworld": self.homeworld.name if self.homeworld else None
            }


class Fav_Planet(db.Model):
    __tablename__="fav_planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))

    __table_args__ = (UniqueConstraint('user_id', 'planet_id', name='_user_planet_uc'),)

    user: Mapped["User"] = relationship(back_populates="fav_planets")
    planet: Mapped["Planet"] = relationship()

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet": self.planet.name if self.planet else None
            }
    

class Fav_Character(db.Model):
    __tablename__="fav_characters"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))

    __table_args__ = (UniqueConstraint('user_id', 'character_id', name='_user_character_uc'),)

    user: Mapped["User"] = relationship(back_populates="fav_characters")
    character: Mapped["Character"] = relationship()

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character": self.character.name if self.character else None
            }
    