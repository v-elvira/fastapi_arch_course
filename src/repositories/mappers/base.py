from src.schemas.common import CommonBaseModel
from src.database import Base

class DataMapper:
    db_model: Base
    schema: CommonBaseModel

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data):
        return cls.db_model(**data.model_dump())
