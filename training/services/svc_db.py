from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
import sqlalchemy.orm as sqla
import config
import pandas as pd
from datetime import datetime


main_dir = config.main_path()
db_file = main_dir / "test.db"

engine = create_engine(f"sqlite:///{db_file}", echo=True, future=True)

mapper_registry = sqla.registry()

Base = mapper_registry.generate_base()
course_csv = pd.read_csv(main_dir / 'course_id.csv')
session = sqla.Session(engine)


class CourseInfo(Base):
    __tablename__ = "course_info"

    id = Column(Integer, unique=True, primary_key=True)
    cohort = Column(String(30))  # Month/Year of Online Cohort
    start_date = Column(DateTime, unique = True)  # First Day of classes opening
    chapter_one_id = Column(Integer, unique=True)  # course id for moodle address.
    chapter_two_id = Column(Integer, unique=True)
    chapter_three_id = Column(Integer, unique=True)
    chapter_four_id = Column(Integer, unique=True)
    chapter_five_id = Column(Integer, unique=True)
    chapter_six_id = Column(Integer, unique=True)
    chapter_seven_id = Column(Integer, unique=True)
    chapter_eight_id = Column(Integer, unique=True)
    chapter_nine_id = Column(Integer, unique=True)
    chapter_ten_id = Column(Integer, unique=True)
    chapter_eleven_id = Column(Integer, unique=True)
    chapter_twelve_id = Column(Integer, unique=True)
    chapter_thirteen_id = Column(Integer, unique=True)
    chapter_fourteen_id = Column(Integer, unique=True)

mapper_registry.metadata.create_all(engine)
# session = Session(engine)
course_csv = course_csv.to_dict(orient='records')
for d in course_csv:
    x = CourseInfo(cohort=d['cohort'],
                   start_date=datetime.strptime(d['start_date'],"%Y-%m-%d").date(),
                   chapter_one_id=d['c1'],
                   chapter_two_id=d['c2'],
                   chapter_three_id=d['c3'],
                   chapter_four_id=d['c4'],
                   chapter_five_id=d['c5'],
                   chapter_six_id=d['c6'],
                   chapter_seven_id=d['c7'],
                   chapter_eight_id=d['c8'],
                   chapter_nine_id=d['c9'],
                   chapter_ten_id=d['c10'],
                   chapter_eleven_id=d['c11'],
                   chapter_twelve_id=d['c12'],
                   chapter_thirteen_id=d['c13'],
                   chapter_fourteen_id=d['c14'])

    session.add(x)
    try:
        session.commit()
    except:
        session.rollback()
    #  class CohortUpdate(Base):
#     __tablename__ = 'cohort_update'

#     id = Column(Integer, primary_key=True)
    
