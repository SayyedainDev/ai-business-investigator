import sys
import os
from datetime import datetime, timezone, timedelta

# Add the project root to the Python path so we can import our app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import engine, Base
from app.db.models import User, Order

def seed_database():
    print("1. Creating database tables from models...")
    # This command looks at models.py and creates the tables in Postgres
    Base.metadata.create_all(bind=engine)

    print("2. Connecting to database to insert data...")
    with Session(engine) as session:
        # Check if data already exists so we don't duplicate it
        if session.query(User).first():
            print("Database is already seeded. Skipping insertion.")
            return

        print("3. Creating Users...")
        user1 = User(email="alice_corp@example.com")
        user2 = User(email="bob_llc@example.com")
        session.add_all([user1, user2])
        session.commit() # Save users so they get IDs

        print("4. Planting Normal History (10 days ago)...")
        past_date = datetime.now(timezone.utc) - timedelta(days=10)
        session.add(Order(user_id=user1.id, total_amount=150.0, status="completed", created_at=past_date))
        session.add(Order(user_id=user2.id, total_amount=200.0, status="completed", created_at=past_date))

        print("5. Planting THE ANOMALY (Yesterday's massive refund spike)...")
        yesterday = datetime.now(timezone.utc) - timedelta(days=1)

        # We are intentionally creating a massive spike in refunds for our AI to discover later
        for _ in range(8):
            session.add(Order(user_id=user1.id, total_amount=499.99, status="refunded", created_at=yesterday))

        session.commit()
        print("Success! Crime scene established. Database is ready for the AI.")

if __name__ == "__main__":
    seed_database()