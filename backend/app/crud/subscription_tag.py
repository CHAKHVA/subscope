from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.subscription_tag import SubscriptionTags
from app.schemas.subscription_tag_link import SubscriptionTagLink


class CRUDSubscriptionTag(CRUDBase[SubscriptionTags, SubscriptionTagLink, SubscriptionTagLink]):
    def create(self, db: Session, *, obj_in: SubscriptionTagLink) -> SubscriptionTags:
        db_obj = SubscriptionTags(
            subscription_id=obj_in.subscription_id,
            tag_id=obj_in.tag_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_subscription_tags(
        self, db: Session, *, subscription_id: int, skip: int = 0, limit: int = 100
    ) -> list[SubscriptionTags]:
        return (
            db.query(self.model)
            .filter(self.model.subscription_id == subscription_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_tag_subscriptions(
        self, db: Session, *, tag_id: int, skip: int = 0, limit: int = 100
    ) -> list[SubscriptionTags]:
        return (
            db.query(self.model)
            .filter(self.model.tag_id == tag_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def delete(
        self, db: Session, *, subscription_id: int, tag_id: int
    ) -> bool:
        result = db.query(self.model).filter(
            self.model.subscription_id == subscription_id,
            self.model.tag_id == tag_id,
        ).delete()
        db.commit()
        return result > 0

    def delete_subscription_tags(
        self, db: Session, *, subscription_id: int
    ) -> bool:
        result = db.query(self.model).filter(
            self.model.subscription_id == subscription_id
        ).delete()
        db.commit()
        return result > 0

    def delete_tag_subscriptions(
        self, db: Session, *, tag_id: int
    ) -> bool:
        result = db.query(self.model).filter(
            self.model.tag_id == tag_id
        ).delete()
        db.commit()
        return result > 0


subscription_tag = CRUDSubscriptionTag(SubscriptionTags)
