from pydantic import BaseModel

class StartupCreate(BaseModel):
    name: str
    industry: str
    arr_range: str
    description: str

class StartupOut(BaseModel):
    id: str
    name: str
    industry: str
    arr_range: str
    description: str
    credibility_score: int

    class Config:
        from_attributes = True
