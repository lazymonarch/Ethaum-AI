from sqlalchemy.orm import Session
from app.startups.models import Startup

def create_startup(db: Session, user_id, data):
    startup = Startup(
        user_id=user_id,
        name=data.name,
        industry=data.industry,
        arr_range=data.arr_range,
        description=data.description,
        credibility_score=0,
    )
    db.add(startup)
    db.commit()
    db.refresh(startup)
    return startup

def get_startup_by_user(db: Session, user_id):
    return db.query(Startup).filter_by(user_id=user_id).first()
