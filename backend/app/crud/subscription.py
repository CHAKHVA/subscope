from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models import Subscription, SubscriptionTag
from app.schemas import SubscriptionCreate, SubscriptionUpdate


class CRUDSubscription(CRUDBase[Subscription, SubscriptionCreate, SubscriptionUpdate]):
    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Subscription]:
        return (
            db.query(self.model)
            .options(
                joinedload(Subscription.subscription_tags).joinedload(
                    SubscriptionTag.tag
                )
            )
            .filter(Subscription.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_user(
        self, db: Session, *, obj_in: SubscriptionCreate, user_id: int
    ) -> Subscription:
        # Create subscription
        db_obj = Subscription(
            user_id=user_id,
            name=obj_in.name,
            amount=obj_in.amount,
            currency=obj_in.currency,
            billing_cycle=obj_in.billing_cycle,
            next_due_date=obj_in.next_due_date,
        )
        db.add(db_obj)
        db.flush()

        # Add tags if provided
        if obj_in.tag_ids:
            for tag_id in obj_in.tag_ids:
                subscription_tag = SubscriptionTag(
                    subscription_id=db_obj.id, tag_id=tag_id
                )
                db.add(subscription_tag)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_user_subscription(
        self, db: Session, *, subscription_id: int, user_id: int
    ) -> Subscription | None:
        return (
            db.query(self.model)
            .options(
                joinedload(Subscription.subscription_tags).joinedload(
                    SubscriptionTag.tag
                )
            )
            .filter(Subscription.id == subscription_id, Subscription.user_id == user_id)
            .first()
        )


subscription = CRUDSubscription(Subscription)
