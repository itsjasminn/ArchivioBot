from sqlalchemy import String, BIGINT, Text, ForeignKey, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.utils import TimeBasedModel, Base


class User(TimeBasedModel):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(VARCHAR(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=True)
    tg_username: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)

    photos: Mapped[list["Photo"]] = relationship("Photo", back_populates="user")
    videos: Mapped[list["Video"]] = relationship("Video", back_populates="user")
    documents: Mapped[list["Document"]] = relationship("Document", back_populates="user")
    letters: Mapped[list["Letter"]] = relationship("Letter", back_populates="user")
    audios: Mapped[list["Audio"]] = relationship("Audio", back_populates="user")
    voices: Mapped[list["Voice"]] = relationship("Voice", back_populates="user")
    contacts: Mapped[list["Contact"]] = relationship("Contact", back_populates="user")

    def __repr__(self):
        return f"User(user_id={self.user_id}, username={self.username})"


class Photo(TimeBasedModel):
    __tablename__ = "photos"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    user: Mapped["User"] = relationship("User", back_populates="photos")
    file_id: Mapped[str] = mapped_column(String(1000), nullable=False)


class Video(TimeBasedModel):
    __tablename__ = "videos"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    user: Mapped["User"] = relationship("User", back_populates="videos")
    file_id: Mapped[str] = mapped_column(String(1000), nullable=False)


class Document(TimeBasedModel):
    __tablename__ = "documents"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    user: Mapped["User"] = relationship("User", back_populates="documents")
    file_id: Mapped[str] = mapped_column(String(1000), nullable=False)


class Letter(TimeBasedModel):
    __tablename__ = "letters"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    user: Mapped["User"] = relationship("User", back_populates="letters")
    content: Mapped[str] = mapped_column(Text, nullable=False)


class Audio(TimeBasedModel):
    __tablename__ = "audios"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    user: Mapped["User"] = relationship("User", back_populates="audios")
    file_id: Mapped[str] = mapped_column(String(1000), nullable=False)


class Voice(TimeBasedModel):
    __tablename__ = "voices"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    user: Mapped["User"] = relationship("User", back_populates="voices")
    file_id: Mapped[str] = mapped_column(String(1000), nullable=False)


class Contact(TimeBasedModel):
    __tablename__ = "contacts"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    user: Mapped["User"] = relationship("User", back_populates="contacts")
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=True)


metadata = Base.metadata
