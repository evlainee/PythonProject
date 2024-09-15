from sqlalchemy import create_engine, Column, Integer, String, Text, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Movie(Base):
    __tablename__ = 'movies'

    movie_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    genre = Column(String(100))
    director = Column(String(100))
    actors = Column(Text)

    sessions = relationship("Session", back_populates="movie")


class Cinema(Base):
    __tablename__ = 'cinemas'

    cinema_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)

    halls = relationship("Hall", back_populates="cinema")


class Hall(Base):
    __tablename__ = 'halls'

    hall_id = Column(Integer, primary_key=True)
    cinema_id = Column(Integer, ForeignKey('cinemas.cinema_id'), nullable=False)
    name = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)

    cinema = relationship("Cinema", back_populates="halls")
    sessions = relationship("Session", back_populates="hall")


class Session(Base):
    __tablename__ = 'sessions'

    session_id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'), nullable=False)
    hall_id = Column(Integer, ForeignKey('halls.hall_id'), nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)

    movie = relationship("Movie", back_populates="sessions")
    hall = relationship("Hall", back_populates="sessions")
    tickets = relationship("Ticket", back_populates="session")


class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20))
    email = Column(String(100))

    tickets = relationship("Ticket", back_populates="customer")


class Ticket(Base):
    __tablename__ = 'tickets'

    ticket_id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.session_id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    seat_number = Column(Integer, nullable=False)
    purchase_time = Column(TIMESTAMP, default='now()')
    price = Column(DECIMAL(10, 2), nullable=False)

    session = relationship("Session", back_populates="tickets")
    customer = relationship("Customer", back_populates="tickets")


# Database configuration
DATABASE_URL = "postgresql://postgres_m:mypassword@10.7.0.5/postgres_m"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

