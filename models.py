from sqlalchemy import Boolean, Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Badge Model
class Badge(Base):
    __tablename__ = "badges"

    id = Column(String, primary_key=True, index=True)
    badge_name = Column(String, index=True)
    attendance_score_threshold = Column(Integer, index=True)
    on_time_threshold = Column(Integer, index=True)
    show_up_rate = Column(Integer, index=True)


# Temp Data Model
class TempData(Base):
    __tablename__ = "csv_data"

    tempid = Column(String, primary_key=True, index=True)
    total_shift = Column(Integer, index=True)
    shift_attended = Column(Integer, index=True)
    attendance_score = Column(Integer, index=True)
    on_time_checkin = Column(Integer, index=True)
    on_time_rate = Column(Integer, index=True)


# Shift Data Model
class ShiftData(Base):
    __tablename__ = "shifts_table"

    id = Column(String, primary_key=True, index=True)
    city = Column(String, index=True)
    state = Column(String, index=True)
    overall_rating = Column(String, index=True)
    speciality = Column(String, index=True)
    certification = Column(String, index=True)
    date = Column(Date, index=True)
    is_long_term = Column(Boolean, index=True)


# SQLAlchemy model for user_credentials table
class UserCredentialsDatabaseModel(Base):
    __tablename__ = "user_credentials"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
