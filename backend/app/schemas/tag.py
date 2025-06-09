from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagInDB(TagBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class Tag(TagInDB):
    pass
