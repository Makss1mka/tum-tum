from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey, Date, UUID, Table
from sqlalchemy.orm import relationship
import datetime

class Base(DeclarativeBase):
    pass


__video_like_association_table = Table(
    "video_likes_association_table",
    Base.metadata,
    Column("video_id", ForeignKey("videos.id"), primary_key=True),
    Column("users_id", ForeignKey("users_data.id"), primary_key=True)
)

__video_tags_association_table = Table(
    "video_tags_association_table",
    Base.metadata,
    Column("video_id", ForeignKey("videos.id"), primary_key=True),
    Column("tag_id", ForeignKey("video_tags.id"), primary_key=True)
)


class VideoTag(Base):
    __tablename__ = "video_tags"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    tag_name = Column(String, nullable=False)

    videos = relationship(
        "Video",
        secondary=__video_tags_association_table,
        back_populates="tags",
        lazy="select"
    )


class VideoStatus(Base):
    __tablename__ = "video_statuses"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    status_name = Column(String, nullable=False)

    videos = relationship("Video", back_populates="status", lazy="select")


class UserData(Base):
    __tablename__ = "users_data",
    id = Column(UUID, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    profile_picture = Column(String, nullable=False)

    videos = relationship("Video", back_populates="author", lazy="select")
    liked_videos = relationship(
        "Video",
        secondary=__video_like_association_table,
        back_populates="liked_users",
        lazy="select"                            
    )


class Video(Base):
    __tablename__ = "videos"
    id = Column(UUID, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    file_video_path = Column(String, nullable=False)
    created_at = Column(Date, nullable=False, default=datetime.datetime.now())
    author_id = Column(UUID, ForeignKey("users_data.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("video_statuses.id"), nullable=False, default=1)

    status = relationship("VideoStatus", back_populates="videos", lazy="select")
    author = relationship("UserData", back_populates="videos", lazy="select")
    liked_users = relationship(
        "UserData",
        secondary=__video_like_association_table,
        back_populates="liked_videos",
        lazy="select"   
    )
    tags = relationship(
        "VideoTag",
        secondary=__video_tags_association_table,
        back_populates="videos",
        lazy="select"
    )

