from sqlmodel import Session, create_engine
from app.crud.user import authenticate
from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

def test_login():
    with Session(engine) as session:
        user = authenticate(
            session=session, 
            email=settings.FIRST_SUPERUSER, 
            password=settings.FIRST_SUPERUSER_PASSWORD
        )
        if user:
            print(f"SUCCESS: Authenticated as {user.email}")
        else:
            print("FAILURE: Could not authenticate")

if __name__ == "__main__":
    test_login()
