
# These lines import necessary modules and libraries, including Click for creating command-line interfaces, and SQLAlchemy for database operations.
import click
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Create an SQLite database
engine = create_engine('sqlite:///book_recommendations.db')

# This line creates a base class Base for declarative class definitions. Declarative base classes are used to define ORM (Object-Relational Mapping) models.

Base = declarative_base()

# Define the User, Book, and ReadingHistory models

# These lines define the User model as an SQLAlchemy ORM class. It represents users in the database and 
# includes fields like 'id' (unique identifier), 'username' (unique username), and establishes a relationship
# with the ReadingHistory model.
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
    book_id = Column(Integer, ForeignKey('books.id'))

Base.metadata.create_all(engine)
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

# This code defines a Click command add_user. It prompts the user to enter a username and adds the user to the 
# database. The click.echo function is used to display a success message.

@cli.command()
@click.option('--username', prompt='Enter your username', help='Username of the user')
def add_reading_history(username):
    user = session.query(User).filter_by(username=username).first()
    if user:
        click.echo(f'User found: {user.username}')
        # It prompts the user to choose between adding a new book or using an existing one.
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
            for i, book in enumerate(existing_books, 1):
                click.echo(f'{i}. Title: {book.title}, Author: {book.author}, Genre: {book.genre}')
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

# Add a command to add books
@cli.command()
@click.option('--title', prompt='Enter the title of the book', help='Title of the book')
@click.option('--author', prompt='Enter the author of the book', help='Author of the book')
@click.option('--genre', prompt='Enter the genre of the book', help='Genre of the book')
def add_book(title, author, genre):
    book = Book(title=title, author=author, genre=genre)
    session.add(book)
    session.commit()
    click.echo(f'Book {title} by {author} added successfully!')

# Modify the view_reading_history command
@cli.command()
@click.option('--username', prompt='Enter username', help='Username of the user')
def view_reading_history(username):
    user = session.query(User).filter_by(username=username).first()
    if user:
        click.echo(f'Reading History for {user.username}:')
        for history in user.reading_history:
            book = session.query(Book).filter_by(id=history.book_id).first()
            click.echo(f'Title: {book.title}, Author: {book.author}, Genre: {book.genre}')
        
        # Recommendations based on genre
        genre_recommendations = session.query(Book).filter_by(genre=book.genre).filter(Book.id != book.id).all()
        if genre_recommendations:
            click.echo(f'\nRecommended Books in Genre: {book.genre}')
            for rec_book in genre_recommendations:
                click.echo(f'Title: {rec_book.title}, Author: {rec_book.author}, Genre: {rec_book.genre}')
        
        # Recommendations based on author
        author_recommendations = session.query(Book).filter_by(author=book.author).filter(Book.id != book.id).all()
        if author_recommendations:
            click.echo(f'\nRecommended Books by Author: {book.author}')
            for rec_book in author_recommendations:
                click.echo(f'Title: {rec_book.title}, Author: {rec_book.author}, Genre: {rec_book.genre}')
    else:
        click.echo('User not found.')

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
            click.echo(f'Username: {user.username}, Books Read: {user.num_books_read}')
    else:
        click.echo('No users found.')

if __name__ == '__main__':
    cli()

# These commands define additional Click commands for viewing reading history, viewing all books, and viewing 
# all users. They provide functionality for interacting with the database and displaying information to the 
# user.