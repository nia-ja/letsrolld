from sqlalchemy import Integer, String, Numeric, DateTime
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, relationship

Base = declarative_base()


director_film_association_table = Table(
    "director_film_association_table",
    Base.metadata,
    Column("film_id", ForeignKey("films.id")),
    Column("director_id", ForeignKey("directors.id")),
)


film_genre_association_table = Table(
    "film_genre_association_table",
    Base.metadata,
    Column("film_id", ForeignKey("films.id")),
    Column("genre_id", ForeignKey("genres.id")),
)


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


film_country_association_table = Table(
    "film_country_association_table",
    Base.metadata,
    Column("film_id", ForeignKey("films.id")),
    Column("country_id", ForeignKey("countries.id")),
)


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    year = Column(Integer, nullable=True)
    rating = Column(Numeric, nullable=True)
    runtime = Column(Integer, nullable=True)

    jw_url = Column(String, nullable=True)
    lb_url = Column(String, nullable=False, unique=True)

    last_updated = Column(DateTime, nullable=True)

    genres: Mapped[list[Genre]] = relationship(
        secondary=film_genre_association_table
    )
    countries: Mapped[list[Country]] = relationship(
        secondary=film_country_association_table
    )


class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    lb_url = Column(String, nullable=False, unique=True)

    last_updated = Column(DateTime, nullable=True)
    last_checked = Column(DateTime, nullable=True)

    films: Mapped[list[Film]] = relationship(
        secondary=director_film_association_table
    )
