from pydantic import BaseModel, ConfigDict


class CommonBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # can be deleted if from_attributes = True used in DataMappers
