
from pydantic import BaseModel

class EvaluationResponse(BaseModel):
    evaluation_success: int # in percentage

