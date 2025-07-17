from pydantic import BaseModel, ConfigDict

class CommonBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes = True)
