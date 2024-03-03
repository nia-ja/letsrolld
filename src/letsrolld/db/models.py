from sqlalchemy import Column, Integer, String, Numeric, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


fd_association_table = Table(
    "film_director_association_table",
    Base.metadata,
    Column("film_id", ForeignKey("films.id")),
    Column("director_id", ForeignKey("directors.id")),
)


class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    year = Column(Integer, nullable=True)
    rating = Column(Numeric, nullable=True)
    runtime = Column(Integer, nullable=True)

    jw_url = Column(String, nullable=True)
    lb_url = Column(String, nullable=True)

    # genres = Column(String)
    # countries = Column(String)


class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    lb_url = Column(String, nullable=True)
