from sqlmodel import SQLModel, Field, create_engine, Session
import pandas as pd

class Major(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    G: str | None = None
    Tournament: str | None = None
    Date: str | None = None
    Location: str | None = None
    P_hash: str | None = Field(alias='P#')
    Winner: str | None = None
    Runner_up: str | None = Field(alias='Runner-up')

engine = create_engine("sqlite:///majors.db")
SQLModel.metadata.create_all(engine)

df = pd.read_csv('majors.csv')
with Session(engine) as session:
    for _, row in df.iterrows():
        major = Major(
            G=row['G'],
            Tournament=row['Tournament'],
            Date=row['Date'],
            Location=row['Location'],
            P_hash=row['P#'],
            Winner=row['Winner'],
            Runner_up=row['Runner-up']
        )
        session.add(major)
    session.commit()