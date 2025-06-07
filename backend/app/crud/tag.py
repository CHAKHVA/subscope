from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Tags
from app.schemas import TagCreate, TagUpdate


class CRUDTag(CRUDBase[Tags, TagCreate, TagUpdate]):
    def create(self, db: Session, *, user_id: int, obj_in: TagCreate) -> Tags:
        obj_data = obj_in.model_dump()
        obj_data["user_id"] = user_id
        tag = Tags(**obj_data)
        try:
            db.add(tag)
            db.commit()
            db.refresh(tag)
        except IntegrityError as err:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag with this name already exists for this user",
            ) from err
        return tag

    def get(self, db: Session, tag_id: int) -> Tags | None:
        return super().get(db, id=tag_id)

    def get_user_tags(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Tags]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self, db: Session, *, tag_id: int, user_id: int, obj_in: TagUpdate
    ) -> Tags:
        db_obj = self.get(db, tag_id)
        if db_obj is None or db_obj.user_id != user_id:
            raise HTTPException(status_code=404, detail="Tag not found")
        try:
            return super().update(db, db_obj=db_obj, obj_in=obj_in)
        except IntegrityError as err:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag with this name already exists for this user",
            ) from err

    def delete(self, db: Session, *, tag_id: int, user_id: int) -> bool:
        db_obj = self.get(db, tag_id)
        if db_obj is None or db_obj.user_id != user_id:
            raise HTTPException(status_code=404, detail="Tag not found")
        db.delete(db_obj)
        db.commit()
        return True


tag = CRUDTag(Tags)
