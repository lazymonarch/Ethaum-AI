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


def get_all_startups(db: Session):
    return db.query(Startup).all()

def discover_startups(
    db,
    industry=None,
    arr_range=None,
    min_score=None,
    sort="credibility",
):
    query = db.query(Startup)

    if industry:
        query = query.filter(Startup.industry == industry)

    if arr_range:
        query = query.filter(Startup.arr_range == arr_range)

    if min_score:
        query = query.filter(Startup.credibility_score >= min_score)

    if sort == "recent":
        query = query.order_by(Startup.created_at.desc())
    else:
        query = query.order_by(Startup.credibility_score.desc())

    return query.all()
