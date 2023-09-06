## Book Recommendations CLI

This command-line interface (CLI) application allows users to manage their reading history, add books, and receive book recommendations based on their reading preferences. The application uses SQLAlchemy to store user data, book information, and reading history in an SQLite database.

## Features

- **Add User**: Add a new user to the database.

- **Add Reading History**: Add books to a user's reading history, with options to add new books or select from existing ones.

- **Add Book**: Add new books to the database.

- **View Reading History**: View a user's reading history, including book recommendations based on the genre and author of the last read book.

- **Recommendations**: Get book recommendations based on genre and author.

- **View All Books**: View a list of all books in the database.

- **View All Users**: View a list of all registered users.



## Usage

- Open the python shell and run `python cli.py`

- You will se various commands:
           - Add user
           - Add Book
           - View all users
           - view all books
           - add reading history
           - view reading history

- To add a new user, use the `add_user` command. You'll be prompted to enter the username.

- To add reading history, use the `add_reading_history` command. You can choose to add a new book or select from existing ones.

- To add a new book, use the `add_book` command. You'll be prompted to enter the title, author, and genre of the book.

- To view reading history and get book recommendations, use the `view_reading_history` command. You'll be prompted to enter the username.

- To view all books, use the `view_all_books` command.

- To view all users, use the `view_all_users` command.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

