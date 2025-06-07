from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.crud.base import CRUDBase
from app.models import Subscriptions
from app.schemas import SubscriptionCreate, SubscriptionUpdate


class CRUDSubscription(CRUDBase[Subscriptions, SubscriptionCreate, SubscriptionUpdate]):
    def create(self, db: Session, *, user_id: int, sub_in: SubscriptionCreate) -> Subscriptions:
        obj_data = sub_in.model_dump()
        obj_data["user_id"] = user_id
        return super().create(db, obj_in=obj_data)

    def get(self, db: Session, subscription_id: int) -> Subscriptions | None:
        return super().get(db, id=subscription_id)

    def get_user_subscriptions(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Subscriptions]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self, db: Session, *, subscription_id: int, user_id: int, sub_in: SubscriptionUpdate
    ) -> Subscriptions:
        db_obj = self.get(db, subscription_id)
        if db_obj is None or db_obj.user_id != user_id:
            raise HTTPException(status_code=404, detail="Subscription not found")
        return super().update(db, db_obj=db_obj, obj_in=sub_in)

    def delete(self, db: Session, *, subscription_id: int, user_id: int) -> bool:
        db_obj = self.get(db, subscription_id)
        if db_obj is None or db_obj.user_id != user_id:
            raise HTTPException(status_code=404, detail="Subscription not found")
        db.delete(db_obj)
        db.commit()
        return True
