# Digital Bulletin Board System

A Python-based digital bulletin board system with user authentication, announcement management, and categorized posts. The application uses CustomTkinter for the GUI and MySQL for data storage.

## Features

- User Authentication (Login/Register)
- Admin and User role separation
- Categorized announcements (Announcements, Events, News)
- Post management (Create, Delete)
- Pin/Unpin announcements
- Clean and modern GUI interface

## Prerequisites

- Python 3.x
- XAMPP (for MySQL database)
- Required Python packages:
  - customtkinter
  - mysql-connector-python
  - CTkMessagebox

## Installation
   
1. Install required Python packages:
   
   ```bash
   pip install customtkinter mysql-connector-python CTkMessagebox
   ```
   
2. Set up the database:
   - Start XAMPP Control Panel
   - Start Apache and MySQL services
   - Open phpMyAdmin (http://localhost/phpmyadmin)
   - Create a new database named `digital_bulletin_db`
   - Click on the `Import` tab
   - Choose the `digital_bulletin_db.sql` file
   - Click "Go" to import the database structure and sample data

## Configuration
In `bulletin.py`, update the database connection settings if needed:
```python
self.connection = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    password="",  # Replace with your MySQL password
    database="digital_bulletin_db"
)
```

## Running the Application
1. Ensure XAMPP's MySQL service is running
2. Run the application:
   ```bash
   python bulletin.py
   ```

## Default Login Credentials
- Admin Account:
  - Username: admin
  - Password: admin
- Sample User Account:
  - Username: user1
  - Password: user1

## Features Description
### User Types
- **Admin**: Can create, delete, and pin/unpin posts in all categories
- **Regular Users**: Can view posts in all categories

### Categories
- **Announcements**: General announcements for all users
- **Events**: Upcoming events or ongoing events
- **News**: News updates and information

### Post Management
- Create new posts with title and content
- Pin important posts to the top
- Delete existing posts (Admin only)
- View posts by category

## Database Structure
### Users Table
- Stores user credentials and information
- Fields: id, username, password (SHA-256 hashed), email, created_at

## Posts Table
- Stores all posts across categories
- Fields: id, title, content, category, date, created_at, pinned

## Troubleshooting
1. Database Connection Error
   - Ensure XAMPP's MySQL service is running
   - Verify database credentials in the code
   - Check if the database and tables exist
2. Module Import Errors
   - Verify all required packages are installed
   - Check Python version compatibility