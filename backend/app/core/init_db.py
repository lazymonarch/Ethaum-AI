from app.core.database import Base, engine
from app.users.models import User
from app.startups.models import Startup
from app.launches.models import Launch
from app.launches.vote_models import LaunchUpvote
from app.reviews.models import Review
from app.feedback.models import EnterpriseFeedback


def init_db():
    Base.metadata.create_all(bind=engine)
