from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Tag
from app.schemas import TagCreate


class CRUDTag(CRUDBase[Tag, TagCreate, TagCreate]):
    def get_by_user(self, db: Session, *, user_id: int) -> list[Tag]:
        return db.query(self.model).filter(Tag.user_id == user_id).all()

    def create_with_user(self, db: Session, *, obj_in: TagCreate, user_id: int) -> Tag:
        db_obj = Tag(user_id=user_id, name=obj_in.name)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_name_and_user(
        self, db: Session, *, name: str, user_id: int
    ) -> Tag | None:
        return (
            db.query(self.model)
            .filter(Tag.name == name, Tag.user_id == user_id)
            .first()
        )

    def get_user_tag(self, db: Session, *, tag_id: int, user_id: int) -> Tag | None:
        return (
            db.query(self.model)
            .filter(Tag.id == tag_id, Tag.user_id == user_id)
            .first()
        )


tag = CRUDTag(Tag)
