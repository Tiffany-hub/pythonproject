# Book Recommendations CLI

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

To use the Book Recommendations CLI, follow these steps:

1. Open your terminal or command prompt.

2. Navigate to the directory where the `cli.py` file is located.

3. Run the CLI application by executing the following command:

4. You will be presented with various commands to interact with the application:
- `add_user`: Add a new user to the database. You'll be prompted to enter the username.

- `add_book`: Add a new book to the database. You'll be prompted to enter the title, author, and genre of the book.

- `view_all_users`: View a list of all registered users.

- `view_all_books`: View a list of all books in the database.

- `add_reading_history`: Add books to a user's reading history, with options to add new books or select from existing ones.

- `view_reading_history`: View a user's reading history and receive book recommendations based on the last read book's genre and author. You'll be prompted to enter the username.

5. Follow the prompts and input the required information to perform the desired actions within the application.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
