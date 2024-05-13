import pandas as pd
from fastapi import HTTPException, status

from logger import setup_logging
from models import Badge, ShiftData, TempData

logger = setup_logging()


# function to get all temps data from temps table
def fetch_temps_data_to_dataframe(db):
    query = db.query(TempData)
    df = pd.read_sql(query.statement, db.bind)
    return df


# function to get all badges data from badges table
def fetch_badge_data_from_db(db):
    badge = db.query(Badge).all()
    if badge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Badge not found"
        )
    return badge


# function to fetch shift data from shifts_table
def fetch_shift_data_to_dataframe(db):
    query = db.query(ShiftData)
    df = pd.read_sql(query.statement, db.bind)
    return df
