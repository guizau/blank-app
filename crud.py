from sqlalchemy.orm import Session
from models import Campaign, Message
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session factory
engine = create_engine('sqlite:///campaigns.db')
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Campaign CRUD operations
def create_campaign(db: Session, name: str, description: str = None):
    campaign = Campaign(name=name, description=description)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign

def get_campaign(db: Session, campaign_id: int):
    return db.query(Campaign).filter(Campaign.id == campaign_id).first()

def get_campaigns(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Campaign).offset(skip).limit(limit).all()

def update_campaign(db: Session, campaign_id: int, name: str = None, description: str = None):
    campaign = get_campaign(db, campaign_id)
    if campaign:
        if name:
            campaign.name = name
        if description is not None:
            campaign.description = description
        db.commit()
        db.refresh(campaign)
    return campaign

def delete_campaign(db: Session, campaign_id: int):
    campaign = get_campaign(db, campaign_id)
    if campaign:
        db.delete(campaign)
        db.commit()
        return True
    return False

# Message CRUD operations
def create_message(db: Session, campaign_id: int, content: str):
    message = Message(
        campaign_id=campaign_id,
        content=content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def get_message(db: Session, message_id: int):
    return db.query(Message).filter(Message.id == message_id).first()

def get_campaign_messages(db: Session, campaign_id: int, skip: int = 0, limit: int = 100):
    return db.query(Message).filter(Message.campaign_id == campaign_id).offset(skip).limit(limit).all()

def update_message(db: Session, message_id: int, content: str = None):
    message = get_message(db, message_id)
    if message:
        if content:
            message.content = content
        db.commit()
        db.refresh(message)
    return message

def delete_message(db: Session, message_id: int):
    message = get_message(db, message_id)
    if message:
        db.delete(message)
        db.commit()
        return True
    return False 