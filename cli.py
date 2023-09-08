import click
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import sqlalchemy
from alembic.config import Config as AlembicConfig
from alembic import command as alembic_command


# Create an SQLite database
engine = create_engine('sqlite:///book_recommendations.db')
Base = sqlalchemy.orm.declarative_base()

# Define the Alembic configuration file path
alembic_ini_path = "alembic.ini"

# Initialize Alembic config
alembic_cfg = AlembicConfig(alembic_ini_path)

# Define the User, Book, and ReadingHistory models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    reading_history = relationship('ReadingHistory', backref='user')

    # New property to calculate the number of books read by the user
    @property
    def num_books_read(self):
        return len(self.reading_history)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)

class ReadingHistory(Base):
    __tablename__ = 'reading_history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))  # Add this line

    book = relationship('Book')  # Add this line


# Create database tables using Alembic migrations
def init_db():
    alembic_command.upgrade(alembic_cfg, "head")

# Initialize the database
init_db()

Session = sessionmaker(bind=engine)
session = Session()

# CLI commands using Click
@click.group()
def cli():
    pass

@cli.command()
@click.option('--username', prompt='Enter username', help='Username of the user')
def add_user(username):
    user = User(username=username)
    session.add(user)
    session.commit()
    click.echo(f'User {username} added successfully!')

@cli.command()
@click.option('--username', prompt='Enter your username', help='Username of the user')
def add_reading_history(username):
    user = session.query(User).filter_by(username=username).first()
    if user:
        click.echo(f'User found: {user.username}')
        choice = input('Do you want to add a new book (N) or use an existing book (E)? ').strip().lower()
        if choice == 'n':
            book_title = input('Enter the title of the book: ')
            author = input('Enter the author of the book: ')
            genre = input('Enter the genre of the book: ')

            book = Book(title=book_title, author=author, genre=genre)
            session.add(book)
            session.commit()
        elif choice == 'e':
            click.echo('Existing books:')
            existing_books = session.query(Book).all()
            for i, existing_book in enumerate(existing_books, 1):
                click.echo(f'{i}. Title: {existing_book.title}, Author: {existing_book.author}, Genre: {existing_book.genre}')
            book_choice = int(input('Select a book by entering its number: '))
            if 1 <= book_choice <= len(existing_books):
                book = existing_books[book_choice - 1]
            else:
                click.echo('Invalid book choice. Using a new book.')
                book_title = input('Enter the title of the book: ')
                author = input('Enter the author of the book: ')
                genre = input('Enter the genre of the book: ')

                book = Book(title=book_title, author=author, genre=genre)
                session.add(book)
                session.commit()
        else:
            click.echo('Invalid choice. Using a new book.')

        reading_history = ReadingHistory(user_id=user.id, book_id=book.id)
        session.add(reading_history)
        session.commit()

        click.echo(f'Book added to reading history for {user.username} successfully!')
    else:
        click.echo('User not found.')

@cli.command()
@click.option('--title', prompt='Enter the title of the book', help='Title of the book')
@click.option('--author', prompt='Enter the author of the book', help='Author of the book')
@click.option('--genre', prompt='Enter the genre of the book', help='Genre of the book')
def add_book(title, author, genre):
    book = Book(title=title, author=author, genre=genre)
    session.add(book)
    session.commit()
    click.echo(f'Book {title} by {author} added successfully!')

@cli.command()
@click.option('--username', prompt='Enter username', help='Username of the user')
def view_reading_history(username):
    user = session.query(User).filter_by(username=username).first()
    if user:
        click.echo(f'Reading History for {user.username}:')
        for history in user.reading_history:
            click.echo(f'Title: {history.book.title}, Author: {history.book.author}, Genre: {history.book.genre}')

        recommend_books(user)

    else:
        click.echo('User not found.')


def recommend_books(user):
    authors = set(history.book.author for history in user.reading_history)
    genres = set(history.book.genre for history in user.reading_history)

    if authors:
        click.echo(f'Recommended Books by Authors:')
        for author in authors:
            books = session.query(Book).filter_by(author=author).all()
            for book in books:
                click.echo(f'Title: {book.title}, Author: {book.author}, Genre: {book.genre}')
    else:
        click.echo('No authors found in reading history.')

    if genres:
        click.echo(f'Recommended Books by Genres:')
        for genre in genres:
            books = session.query(Book).filter_by(genre=genre).all()
            for book in books:
                click.echo(f'Title: {book.title}, Author: {book.author}, Genre: {book.genre}')
    else:
        click.echo('No genres found in reading history.')

@cli.command()
def view_all_books():
    books = session.query(Book).all()
    if books:
        click.echo('All Books:')
        for book in books:
            click.echo(f'Title: {book.title}, Author: {book.author}, Genre: {book.genre}')
    else:
        click.echo('No books found.')

@cli.command()
def view_all_users():
    users = session.query(User).all()
    if users:
        click.echo('All Users:')
        for user in users:
            click.echo(f'Username: {user.username}, Number of Books Read: {user.num_books_read}')
    else:
        click.echo('No users found.')

if __name__ == '__main__':
    cli()
