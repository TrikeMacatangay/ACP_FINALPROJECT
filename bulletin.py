import sys
import customtkinter as ctk
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import hashlib
import re
from CTkMessagebox import CTkMessagebox

# Database connection and management class
class DatabaseConnection:
    def __init__(self):
        self.connection = None
        if not self.connect():
            raise ConnectionError("Failed to connect to database")

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="digital_bulletin_db"
            )
            if self.connection.is_connected():
                print("Successfully connected to database")
                return True
        except Error as e:
            print(f"Database connection error: {e}")
            return False
        return False

    def ensure_connection(self):
        """Ensures database connection is active and reconnects if necessary"""
        try:
            if not self.connection or not self.connection.is_connected():
                print("Database connection lost, reconnecting...")
                if not self.connect():
                    raise ConnectionError("Failed to reconnect to database")
        except Error as e:
            print(f"Database connection error: {e}")
            raise ConnectionError("Database connection error")

    def fetch_announcements(self, category):
        """Fetches and returns all posts for a given category, ordered by pin status and date"""
        self.ensure_connection()
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(
                """SELECT * FROM posts 
                   WHERE category = %s 
                   ORDER BY pinned DESC, date DESC, id DESC""",
                (category,)
            )
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching posts: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            self.connection.commit()

    def toggle_pin(self, announcement_id):
        """Toggles the pinned status of a post"""
        self.ensure_connection()
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """UPDATE posts 
                   SET pinned = NOT pinned 
                   WHERE id = %s""",
                (announcement_id,)
            )
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error toggling pin: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            self.connection.commit()

    def verify_login(self, username, password):
        """Verifies user credentials and returns (success, is_admin) tuple"""
        self.ensure_connection()
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute(
                "SELECT * FROM users WHERE username = %s AND password = %s",
                (username, hashed_password)
            )
            user = cursor.fetchone()
            return (user is not None, username == 'admin')
        except Error as e:
            print(f"Error: {e}")
            return (False, False)
        finally:
            if cursor:
                cursor.close()
            self.connection.commit()

    def register_user(self, username, password, email):
        """Creates a new user account with hashed password"""
        self.ensure_connection()
        cursor = None
        try:
            cursor = self.connection.cursor()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                (username, hashed_password, email)
            )
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            self.connection.commit()

    def post_announcement(self, title, content, category, date, pinned=False):
        return self.create_post(title, content, category, date, pinned)

    def create_post(self, title, content, category, date, pinned=False):
        self.ensure_connection()
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO posts (title, content, category, date, pinned) VALUES (%s, %s, %s, %s, %s)",
                (title, content, category, date, pinned)
            )
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error creating post: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def delete_announcement(self, id):
        return self.delete_post(id)

    def delete_post(self, id):
        self.ensure_connection()
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "DELETE FROM posts WHERE id = %s",
                (id,)
            )
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error deleting post: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            self.connection.commit()

# Login page UI class
class LoginPage(ctk.CTkFrame):
    """Handles user authentication interface"""
    def __init__(self, parent, on_login, on_register):
        super().__init__(parent)
        self.db = parent.db
        
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both")
        
        login_frame = ctk.CTkFrame(container)
        login_frame.pack(pady=(50, 0))
        
        self.title = ctk.CTkLabel(login_frame, text="Login", font=("Helvetica", 24, "bold"))
        self.title.pack(pady=(20, 15))
        
        self.username = ctk.CTkEntry(login_frame, placeholder_text="Username", width=250, height=35)
        self.username.pack(pady=10, padx=30)
        
        self.password = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*", width=250, height=35)
        self.password.pack(pady=10, padx=30)
        
        self.login_btn = ctk.CTkButton(login_frame, text="Login", width=250, height=35, command=self.login)
        self.login_btn.pack(pady=10)
        
        self.register_btn = ctk.CTkButton(
            login_frame, 
            text="Register", 
            command=on_register,
            fg_color="transparent",
            border_width=2,
            width=250,
            height=35
        )
        self.register_btn.pack(pady=(5, 20))
        
        self.on_login = on_login

    def login(self):
        success, is_admin = self.db.verify_login(self.username.get(), self.password.get())
        if success:
            self.on_login(is_admin)
        else:
            CTkMessagebox(
                title="Login Failed",
                message="Invalid username or password!",
                icon="cancel"
            )

# User registration page UI class
class RegisterPage(ctk.CTkFrame):
    """Handles new user registration interface"""
    def __init__(self, parent, on_back):
        super().__init__(parent)
        self.db = parent.db
        self.on_back = on_back
        
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both")
        
        register_frame = ctk.CTkFrame(container)
        register_frame.pack(pady=(50, 0))
        
        self.title = ctk.CTkLabel(register_frame, text="Register", font=("Helvetica", 24, "bold"))
        self.title.pack(pady=(20, 15))
        
        self.username = ctk.CTkEntry(register_frame, placeholder_text="Username", width=250, height=35)
        self.username.pack(pady=10, padx=30)
        
        self.email = ctk.CTkEntry(register_frame, placeholder_text="Email", width=250, height=35)
        self.email.pack(pady=10, padx=30)
        
        self.password = ctk.CTkEntry(register_frame, placeholder_text="Password", show="*", width=250, height=35)
        self.password.pack(pady=10, padx=30)
        
        self.register_btn = ctk.CTkButton(register_frame, text="Register", width=250, height=35, command=self.register)
        self.register_btn.pack(pady=10)
        
        self.back_btn = ctk.CTkButton(
            register_frame, 
            text="Back to Login", 
            command=on_back,
            fg_color="transparent",
            border_width=2,
            width=250,
            height=35
        )
        self.back_btn.pack(pady=(5, 20))

    def validate_email(self, email):
        """Validates email format using regex pattern"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def register(self):
        username = self.username.get()
        password = self.password.get()
        email = self.email.get()

        if not username or not password or not email:
            CTkMessagebox(
                title="Registration Error",
                message="All fields are required!",
                icon="cancel"
            )
            return

        if not self.validate_email(email):
            CTkMessagebox(
                title="Registration Error",
                message="Please enter a valid email address!",
                icon="cancel"
            )
            return

        if self.db.register_user(username, password, email):
            msg = CTkMessagebox(
                title="Success",
                message="Registration successful!\nDo you want to login now?",
                icon="check",
                option_2="Yes",
                option_1="No"
            )
            if msg.get() == "Yes":
                self.on_back()
        else:
            CTkMessagebox(
                title="Registration Error",
                message="Registration failed!\nUsername or email might already exist.",
                icon="cancel"
            )

# Main application window class
class BulletinBoard(ctk.CTk):
    """Main application window handling all UI components and logic"""
    def __init__(self):
        ctk.set_appearance_mode("dark")
        super().__init__()
        self.title("Barangay Digital Bulletin Board")
        self.geometry("800x600")
        self.resizable(False, False)
        
        self.db = DatabaseConnection()
        
        self.show_login() 

    def show_login(self):
        self.clear_window()
        self.login_page = LoginPage(self, lambda is_admin: self.show_main_content(is_admin), self.show_register)
        self.login_page.pack(expand=True, fill="both", padx=20, pady=20)

    def show_register(self):
        self.clear_window()
        self.register_page = RegisterPage(self, self.show_login)
        self.register_page.pack(expand=True, fill="both", padx=20, pady=20)

    def show_main_content(self, is_admin=False):
        """Creates and displays the main bulletin board interface
        
        Args:
            is_admin (bool): Determines if admin features should be shown
        """
        self.clear_window()
        self.is_admin = is_admin
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.grid(row=0, column=0, padx=(10,0), pady=10, sticky="nsew")
        self.sidebar.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="Categories",
            font=("Helvetica", 20, "bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20,10))

        self.announcements_btn = ctk.CTkButton(
            self.sidebar, text="Announcements",
            command=lambda: self.show_category("Announcements")
        )
        self.events_btn = ctk.CTkButton(
            self.sidebar, text="Events",
            command=lambda: self.show_category("Events")
        )
        self.news_btn = ctk.CTkButton(
            self.sidebar, text="News",
            command=lambda: self.show_category("News")
        )

        self.announcements_btn.grid(row=1, column=0, padx=20, pady=10)
        self.events_btn.grid(row=2, column=0, padx=20, pady=10)
        self.news_btn.grid(row=3, column=0, padx=20, pady=10)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        self.header = ctk.CTkLabel(
            header_frame,
            text="",
            font=("Helvetica", 24, "bold")
        )
        self.header.pack(side="left", pady=10)
        
        if self.is_admin:
            self.post_btn = ctk.CTkButton(
                header_frame,
                text="+ New Post",
                command=lambda: self.show_post_dialog(self.header.cget("text")),
                fg_color="#28a745",
                font=("Helvetica", 12, "bold")
            )
            self.post_btn.pack(side="right", padx=20)

        self.content_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.logout_btn = ctk.CTkButton(
            self.sidebar,
            text="Logout",
            command=self.show_login,
            fg_color="transparent",
            border_width=2,
            text_color="red"
        )
        self.logout_btn.grid(row=6, column=0, padx=20, pady=(0, 10), sticky="s")

        self.show_category("Announcements")

    def show_category(self, category):
        try:
            announcements = self.db.fetch_announcements(category)
            if announcements is None:
                announcements = []
                
            self.header.configure(text=category)
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            
            self.display_announcements(announcements)
            
        except Exception as e:
            print(f"Error showing category: {e}")
            self.header.configure(text=category)
            ctk.CTkLabel(
                self.content_frame,
                text="Error loading content. Please try again.",
                font=("Helvetica", 14)
            ).pack(pady=20)

    def display_announcements(self, announcements):
        """Renders announcements in the content area with pin/delete options for admins
        
        Args:
            announcements (list): List of announcement dictionaries to display
        """
        if not announcements:
            ctk.CTkLabel(
                self.content_frame,
                text="No announcements available",
                font=("Helvetica", 14)
            ).pack(pady=20)
            return

        for ann in announcements:
            frame = ctk.CTkFrame(self.content_frame)
            frame.pack(fill="x", pady=5, padx=10)
            
            title_frame = ctk.CTkFrame(frame, fg_color="transparent")
            title_frame.pack(fill="x", padx=15, pady=(15,5))
            
            header_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
            header_frame.pack(fill="x")

            if self.is_admin:
                admin_buttons = ctk.CTkFrame(header_frame, fg_color="transparent")
                admin_buttons.place(relx=1.0, rely=0.5, anchor="e", x=-5)

                def toggle_pin(post_id=ann["id"]):
                    if self.db.toggle_pin(post_id):
                        self.show_category(self.header.cget("text"))

                pin_text = "📌" if not ann.get("pinned") else "❌"
                pin_btn = ctk.CTkButton(
                    admin_buttons,
                    text=pin_text,
                    width=30,
                    height=30,
                    fg_color="transparent",
                    text_color="gray",
                    hover_color="#E6E6E6",
                    command=toggle_pin
                )
                pin_btn.pack(side="left", padx=5)

                def delete_post(post_id=ann["id"]):
                    if CTkMessagebox(
                        title="Confirm Delete",
                        message="Are you sure you want to delete this post?",
                        icon="warning",
                        option_1="Cancel",
                        option_2="Delete"
                    ).get() == "Delete":
                        if self.db.delete_post(post_id):
                            self.show_category(self.header.cget("text"))
                
                delete_btn = ctk.CTkButton(
                    admin_buttons,
                    text="×",
                    width=30,
                    height=30,
                    fg_color="transparent",
                    text_color="red",
                    hover_color="#FFE6E6",
                    command=delete_post
                )
                delete_btn.pack(side="left")

            title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
            title_container.pack(expand=True, fill="x", padx=(70, 70))
            
            title_text = ann["title"]
            if ann.get("pinned"):
                title_text = "📌 " + title_text

            title_label = ctk.CTkLabel(
                title_container,
                text=title_text,
                font=("Helvetica", 16, "bold"),
                justify="center",
                anchor="center"
            )
            title_label.pack(expand=True, anchor="center")

            # Date formatting and display
            date_str = ann['date']
            if isinstance(date_str, str):
                try:
                    # Convert string date to formatted display
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    formatted_date = date_obj.strftime('%B %d, %Y')
                except ValueError:
                    formatted_date = date_str
            else:
                formatted_date = date_str.strftime('%B %d, %Y')

            date_label = ctk.CTkLabel(
                title_frame,
                text=formatted_date,
                font=("Helvetica", 12),
                text_color="gray"
            )
            date_label.pack(pady=(5,0))
            
            separator = ctk.CTkFrame(frame, height=1, fg_color="gray75")
            separator.pack(fill="x", padx=15, pady=(5,10))
            
            content = ann.get("content", "")
            content_label = ctk.CTkLabel(
                frame,
                text=content,
                wraplength=600,
                justify="left",
                anchor="w"
            )
            content_label.pack(padx=15, pady=(0,15), fill="x")

    def show_post_form(self, category):
        """Displays the form for creating new announcements
        
        Args:
            category (str): Category of the post being created
        """
        self.clear_window()
        
        outer_frame = ctk.CTkFrame(self)
        outer_frame.pack(expand=True, fill="both")
        
        container = ctk.CTkFrame(outer_frame)
        container.pack(expand=True, padx=100, pady=50)
        
        header = ctk.CTkLabel(
            container,
            text=f"Post New {category}",
            font=("Helvetica", 24, "bold")
        )
        header.pack(pady=(20, 30))
        
        form_container = ctk.CTkFrame(container, fg_color="transparent")
        form_container.pack(padx=100, fill="both", expand=True)
        
        ctk.CTkLabel(form_container, text="Title:", anchor="w").pack(fill="x")
        title_entry = ctk.CTkEntry(form_container, width=400)
        title_entry.pack(pady=(0, 15))
        
        ctk.CTkLabel(form_container, text="Content:", anchor="w").pack(fill="x")
        content_text = ctk.CTkTextbox(form_container, width=400, height=200)
        content_text.pack(pady=(0, 15))
        
        button_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 20))
        
        def post_announcement():
            title = title_entry.get().strip()
            content = content_text.get("1.0", "end-1c").strip()
            current_date = datetime.now().strftime('%Y-%m-%d')
            
            if not all([title, content]):
                CTkMessagebox(
                    title="Error",
                    message="All fields are required!",
                    icon="cancel"
                )
                return
                
            try:
                if self.db.create_post(title, content, category, current_date):
                    msg = CTkMessagebox(
                        title="Success",
                        message=f"New {category} post added successfully!",
                        icon="check",
                        option_1="OK"
                    )
                    if msg.get() == "OK":
                        self._return_to_main(category)
                else:
                    CTkMessagebox(
                        title="Error",
                        message=f"Failed to add {category} post!",
                        icon="cancel"
                    )
            except Exception as e:
                print(f"Error posting {category}: {e}")
                CTkMessagebox(
                    title="Error",
                    message="An error occurred while posting!",
                    icon="cancel"
                )

        back_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=lambda: self.show_main_content(self.is_admin),
            width=100,
            fg_color="transparent",
            border_width=1
        )
        back_btn.pack(side='left', padx=(0, 10))
        
        post_btn = ctk.CTkButton(
            button_frame,
            text="Post Announcement",
            command=post_announcement,
            width=150,
            fg_color="#28a745"
        )
        post_btn.pack(side='right')

    def show_post_dialog(self, category):
        self.show_post_form(category)

    def _return_to_main(self, category):
        try:
            self.show_main_content(self.is_admin)
            self.show_category(category)
        except Exception as e:
            print(f"Error returning to main view: {e}")
            self.show_login()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

# Application entry point
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    
    # Initialize application with error handling for database connection
    try:
        app = BulletinBoard()
        app.mainloop()
    except ConnectionError as e:
        try:
            root = ctk.CTk()
            root.withdraw()
            CTkMessagebox(
                title="Database Error",
                message="Could not connect to database.\nPlease ensure MySQL is running and try again.",
                icon="cancel",
                option_1="Exit"
            )
            root.destroy()
        except:
            print("ERROR: Could not connect to database. Please ensure MySQL is running.")
        sys.exit(1)