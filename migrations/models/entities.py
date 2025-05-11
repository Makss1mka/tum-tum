from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Date, UUID, Integer, ForeignKey, Table, Uuid
from sqlalchemy.orm import relationship
import datetime

class Base(DeclarativeBase):
    pass


#
# ASSOCIATION TABLES
#

video_like_association_table = Table(
    "video_likes_association_table",
    Base.metadata,
    Column("video_id", ForeignKey("videos.id"), primary_key=True),
    Column("users_id", ForeignKey("users_data.id"), primary_key=True)
)

video_tags_association_table = Table(
    "video_tags_association_table",
    Base.metadata,
    Column("video_id", ForeignKey("videos.id"), primary_key=True),
    Column("tag_id", ForeignKey("video_tags.id"), primary_key=True)
)



#
# USER'S MODELS
#

class UserCredits(Base):
    __tablename__ = "users_credits"
    id = Column(UUID, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(Date, nullable=False, default=datetime.datetime.now())
    role_id = Column(Integer, ForeignKey("users_roles.id"), nullable=False, default=0)

    role = relationship("Role", back_populates="users", lazy="select")

class UserData(Base):
    __tablename__ = "users_data"
    id = Column(UUID, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    profile_picture = Column(String, nullable=False)

    videos = relationship("Video", back_populates="author", lazy="select")
    liked_videos = relationship(
        "Video",
        secondary=video_like_association_table,
        back_populates="liked_users",
        lazy="select"                            
    )

class Role(Base):
    __tablename__ = "users_roles"
    id = Column(Integer, nullable=False, primary_key=True)
    role = Column(String, nullable=False)

    users = relationship("UserCredits", back_populates="role", lazy="select")



#
# VIDEO'S MODELS
#

class VideoTags(Base):
    __tablename__ = "video_tags"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    tag_name = Column(String, nullable=False)

    videos = relationship(
        "Video",
        secondary=video_tags_association_table,
        back_populates="tags",
        lazy="select"
    )

class Video(Base):
    __tablename__ = "videos"
    id = Column(UUID, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    author_id = Column(UUID, ForeignKey("users_data.id"), nullable=False)

    author = relationship("UserData", back_populates="videos", lazy="select")
    liked_users = relationship(
        "UserData",
        secondary=video_like_association_table,
        back_populates="liked_videos" ,
        lazy="select"   
    )
    tags = relationship(
        "VideoTags",
        secondary=video_tags_association_table,
        back_populates="videos",
        lazy="select"
    )



