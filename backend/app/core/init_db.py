from app.core.database import Base, engine
from app.users.models import User
from app.startups.models import Startup

def init_db():
    Base.metadata.create_all(bind=engine)
