from sqlalchemy import Integer, String, Numeric, DateTime
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, relationship

Base = declarative_base()


film_genre_association_table = Table(
    "film_genre_association_table",
    Base.metadata,
    Column("film_id", ForeignKey("films.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
)


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


film_country_association_table = Table(
    "film_country_association_table",
    Base.metadata,
    Column("film_id", ForeignKey("films.id"), primary_key=True),
    Column("country_id", ForeignKey("countries.id"), primary_key=True),
)


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


film_offer_association_table = Table(
    "film_offer_association_table",
    Base.metadata,
    Column("film_id", ForeignKey("films.id"), primary_key=True),
    Column("offer_id", ForeignKey("offers.id"), primary_key=True),
)


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


director_film_association_table = Table(
    "director_film_association_table",
    Base.metadata,
    Column("film_id", ForeignKey("films.id"), primary_key=True),
    Column("director_id", ForeignKey("directors.id"), primary_key=True),
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
    lb_url = Column(String, nullable=False, unique=True)
    trailer_url = Column(String, nullable=True)

    last_updated = Column(DateTime, nullable=True)
    last_checked = Column(DateTime, nullable=True)
    last_offers_checked = Column(DateTime, nullable=True)
    last_offers_updated = Column(DateTime, nullable=True)

    genres: Mapped[list[Genre]] = relationship(secondary=film_genre_association_table)
    countries: Mapped[list[Country]] = relationship(
        secondary=film_country_association_table
    )
    offers: Mapped[list[Offer]] = relationship(secondary=film_offer_association_table)

    directors = relationship(
        "Director",
        secondary=director_film_association_table,
        back_populates="films",
    )

    @property
    def name(self):
        return self.title


class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    lb_url = Column(String, nullable=False, unique=True)

    last_updated = Column(DateTime, nullable=True)
    last_checked = Column(DateTime, nullable=True)

    films = relationship("Film", secondary=director_film_association_table)
