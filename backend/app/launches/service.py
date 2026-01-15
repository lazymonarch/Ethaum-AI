from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.launches.models import Launch
from app.launches.vote_models import LaunchUpvote
from app.startups.models import Startup
from app.startups.credibility import calculate_credibility

def create_launch(db: Session, startup_id, data):
    launch = Launch(
        startup_id=startup_id,
        title=data.title,
        tagline=data.tagline,
        description=data.description,
    )
    db.add(launch)
    db.commit()
    db.refresh(launch)

    startup = db.query(Startup).filter_by(id=startup_id).first()
    if startup:
        calculate_credibility(db, startup)
    
    return launch


def list_launches(db: Session):
    return db.query(Launch).order_by(Launch.upvotes.desc()).all()


def upvote_launch(db: Session, launch_id, user_id):
    vote = LaunchUpvote(
        launch_id=launch_id,
        user_id=user_id,
    )
    db.add(vote)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Already upvoted")

    # increment counter
    launch = db.query(Launch).filter_by(id=launch_id).first()
    launch.upvotes += 1
    db.commit()
    
    # Calculate credibility after upvote
    calculate_credibility(db, launch.startup)
    
    return launch
