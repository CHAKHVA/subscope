from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.crud.base import CRUDBase
from app.models import Tags
from app.schemas import TagCreate


class CRUDTag(CRUDBase[Tags, TagCreate, TagCreate]):
    def create(self, db: Session, *, user_id: int, tag_in: TagCreate) -> Tags:
        tag_data = tag_in.model_dump()
        tag_data["user_id"] = user_id
        tag = Tags(**tag_data)
        try:
            db.add(tag)
            db.commit()
            db.refresh(tag)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag with this name already exists for this user",
            )
        return tag

    def get(self, db: Session, tag_id: int) -> Tags | None:
        return db.query(Tags).filter(Tags.id == tag_id).first()

    def get_user_tags(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Tags]:
        return (
            db.query(Tags)
            .filter(Tags.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self, db: Session, *, tag_id: int, user_id: int, tag_in: TagCreate
    ) -> Tags:
        tag = self.get(db, tag_id)
        if not tag or tag.user_id != user_id:
            raise HTTPException(status_code=404, detail="Tag not found")
        for key, value in tag_in.model_dump().items():
            setattr(tag, key, value)
        try:
            db.commit()
            db.refresh(tag)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag with this name already exists for this user",
            )
        return tag

    def delete(self, db: Session, *, tag_id: int, user_id: int) -> bool:
        tag = self.get(db, tag_id)
        if not tag or tag.user_id != user_id:
            raise HTTPException(status_code=404, detail="Tag not found")
        db.delete(tag)
        db.commit()
        return True


tag_crud = CRUDTag(Tags)
