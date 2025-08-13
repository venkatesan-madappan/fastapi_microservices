from config.db.db_setup import Base
from sqlalchemy import Column, String, Integer, Date, ForeignKey, Float
from sqlalchemy.orm import relationship

class Login(Base): 
    __tablename__ = "login"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=False, index=False, nullable=False)
    password = Column(String, unique=False, index=False, nullable=False)
    user_type = Column(Integer, unique=False, index=False, nullable=False)
    
class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, unique=False, index=False, nullable=False)
    lastname = Column(String, unique=False, index=False, nullable=False)
    age = Column(Integer, unique=False, index=False, nullable=False)
    date_started = Column(Date, unique=False, index=False, nullable=False)
    status = Column(Integer, unique=False, index=False, nullable=False)
    login_id = Column(Integer, ForeignKey('login.id'), unique=False, index=False, nullable=False)
    birthday = Column(Date, unique=False, index=False, nullable=False)
    # login = relationship("Login", back_populates="admin")

class Vendor(Base): 
    __tablename__ = "vendor"
    id = Column(Integer, primary_key=True, index=True)
    rep_firstname = Column(String, unique=False, index=False, nullable=False)
    rep_lastname = Column(String, unique=False, index=False, nullable=False)
    rep_id = Column(String, unique=False, index=False, nullable=False)
    rep_date_employed = Column(Date, unique=False, index=False, nullable=False)
    account_name = Column(String, unique=False, index=False, nullable=False)
    account_number = Column(String, unique=False, index=False, nullable=False)
    date_consigned = Column(Date, unique=False, index=False, nullable=False)
    login_id = Column(Integer, ForeignKey('login.id'), unique=False, index=False, nullable=False) 

class Customer(Base): 
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, unique=False, index=False, nullable=False)
    lastname = Column(String, unique=False, index=False, nullable=False)
    age = Column(Integer, unique=False, index=False, nullable=False)
    birthday = Column(Date, unique=False, index=False, nullable=False)
    date_subscribed = Column(Date, unique=False, index=False, nullable=False)
    status = Column(Integer, unique=False, index=False, nullable=False)
    subscription_type = Column(Integer, unique=False, index=False, nullable=False)
    login_id = Column(Integer, ForeignKey('login.id'), unique=False, index=False, nullable=False) 

class Billing(Base):
    __tablename__ = "billing"
    id = Column(Integer, primary_key=True, index=True)
    payable = Column(Float, unique=False, index=False, nullable=False)
    approved_by = Column(String, unique=False, index=False, nullable=False)
    date_approved = Column(Date, unique=False, index=False, nullable=False)
    date_billed = Column(Date, unique=False, index=False, nullable=False)
    received_by = Column(String, unique=False, index=False, nullable=False)
    date_received = Column(Date, unique=False, index=False, nullable=False)
    total_issues = Column(Integer, unique=False, index=False, nullable=False)
    vendor_id = Column(Integer, ForeignKey('vendor.id'), unique=False, index=False, nullable=False) 
    admin_id = Column(Integer, ForeignKey('admin.id'), unique=False, index=False, nullable=False) 

class Messenger(Base): 
    __tablename__ = "messenger"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, unique=False, index=False, nullable=False)
    lastname = Column(String, unique=False, index=False, nullable=False)
    salary = Column(Float, unique=False, index=False, nullable=False)
    date_employed = Column(Date, unique=False, index=False, nullable=False)
    status = Column(Integer, unique=False, index=False, nullable=False)
    vendor_id = Column(Integer, ForeignKey('vendor.id'), unique=False, index=False, nullable=False)  

class Publication(Base):
    __tablename__ = "publication"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False, index=False, nullable=False)
    type = Column(String, unique=False, index=False, nullable=False)
    vendor_id = Column(Integer, ForeignKey('vendor.id'), unique=False, index=False, nullable=False)  
    messenger_id = Column(Integer, ForeignKey('messenger.id'), unique=False, index=False, nullable=False)      

class Content(Base):
    __tablename__ = "content"
    id = Column(Integer,  primary_key=True, index=True)
    publication_id = Column(Integer, ForeignKey('publication.id'), unique=False, index=False, nullable=False)
    headline = Column(String, unique=False, index=False, nullable=False)
    content = Column(String, unique=False, index=False, nullable=False)
    content_type = Column(String, unique=False, index=False, nullable=False)
    date_published = Column(Date, unique=False, index=False, nullable=False)

class Sales(Base):
    __tablename__ = "sales"
    id = Column(Integer,  primary_key=True, index=True)
    publication_id = Column(Integer, ForeignKey('publication.id'), unique=False, index=False, nullable=False)
    copies_issued = Column(Integer, unique=False, index=False, nullable=False)
    copies_sold = Column(Integer, unique=False, index=False, nullable=False)
    date_issued = Column(Date, unique=False, index=False, nullable=False)
    revenue = Column(Float, unique=False, index=False, nullable=False)
    profit = Column(Float, unique=False, index=False, nullable=False)

class Subscription(Base):
    __tablename__ = "subscription"
    id = Column(Integer,  primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), unique=False, index=False, nullable=False)
    branch = Column(String, unique=False, index=False, nullable=False)
    price = Column(Float, unique=False, index=False, nullable=False)
    qty = Column(Integer, unique=False, index=False, nullable=False)
    date_purchased = Column(Date, unique=False, index=False, nullable=False)
