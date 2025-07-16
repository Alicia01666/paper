import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet
import os


# Encryption Functions
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    return open("secret.key", "rb").read()


def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data


def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data


def save_passwords(passwords, key, current):
    encrypted_passwords = []
    for website, username, password in passwords:
        encrypted_website = encrypt_data(website, key)
        encrypted_username = encrypt_data(username, key)
        encrypted_password = encrypt_data(password, key)
        encrypted_passwords.append(
            (encrypted_website, encrypted_username, encrypted_password)
        )

    with open(f"data/{current}.enc", "wb") as file:
        for (
            encrypted_website,
            encrypted_username,
            encrypted_password,
        ) in encrypted_passwords:
            file.write(encrypted_website + b"\n")
            file.write(encrypted_username + b"\n")
            file.write(encrypted_password + b"\n")


def save_users(users, key):
    encrypted_users = []
    for user, passwd in users.items():
        encrypt_user = encrypt_data(user, key)
        encrypt_passwd = encrypt_data(passwd, key)
        encrypted_users.append((encrypt_user, encrypt_passwd))

    with open("data/users.enc", "wb") as file:
        for user, passwd in encrypted_users:
            file.write(user + b"\n")
            file.write(passwd + b"\n")


def load_passwords(key, current):
    if not os.path.exists(f"data/{current}.enc"):
        return []

    with open(f"data/{current}.enc", "rb") as file:
        lines = file.readlines()

    passwords = []
    for i in range(0, len(lines), 3):
        encrypted_website = lines[i].strip()
        encrypted_username = lines[i + 1].strip()
        encrypted_password = lines[i + 2].strip()

        website = decrypt_data(encrypted_website, key)
        username = decrypt_data(encrypted_username, key)
        password = decrypt_data(encrypted_password, key)

        passwords.append((website, username, password))

    return passwords


def load_users(key):
    if not os.path.exists("data/users.enc"):
        return {}
    with open("data/users.enc", "rb") as file:
        lines = file.readlines()

    users = {}
    for i in range(0, len(lines), 2):
        euser = lines[i].strip()
        epass = lines[i + 1].strip()

        user = decrypt_data(euser, key)
        passwd = decrypt_data(epass, key)
        users[user] = passwd
    return users


class PasswordManager:
    def __init__(self, root):
        if not os.path.exists("data"):
            os.mkdir("data")
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("600x400")
        self.root.configure(bg="#2E3440")  # Dark background
        self.hide_password = True

        # Load or generate encryption key
        if not os.path.exists("secret.key"):
            generate_key()
        self.key = load_key()

        self.users = load_users(self.key)
        self.current_user = None
        self.passwords = []  # Simulated password storage
        self.show_login_page()

    def show_login_page(self):
        self.clear_window()
        self.root.geometry("400x300")

        # Title
        title_label = ttk.Label(
            self.root,
            text="Login",
            font=("Helvetica", 20, "bold"),
            foreground="#ECEFF4",
            background="#2E3440",
        )
        title_label.pack(pady=20)

        # Username
        username_label = ttk.Label(
            self.root, text="Username:", foreground="#ECEFF4", background="#2E3440"
        )
        username_label.pack()
        self.username_entry = ttk.Entry(self.root, width=30)
        self.username_entry.pack(pady=5)

        # Password
        password_label = ttk.Label(
            self.root, text="Password:", foreground="#ECEFF4", background="#2E3440"
        )
        password_label.pack()
        self.password_entry = ttk.Entry(self.root, width=30, show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        login_button = ttk.Button(
            self.root, text="Login", command=self.login, style="Accent.TButton"
        )
        login_button.pack(pady=10)

        # Signup Link
        signup_label = ttk.Label(
            self.root,
            text="Don't have an account? Sign up",
            cursor="hand2",
            foreground="#81A1C1",
            background="#2E3440",
        )
        signup_label.pack(pady=5)
        signup_label.bind("<Button-1>", lambda e: self.show_signup_page())

    def show_signup_page(self):
        self.clear_window()
        self.root.geometry("400x300")

        # Title
        title_label = ttk.Label(
            self.root,
            text="Sign Up",
            font=("Helvetica", 20, "bold"),
            foreground="#ECEFF4",
            background="#2E3440",
        )
        title_label.pack(pady=20)

        # Username
        username_label = ttk.Label(
            self.root, text="Username:", foreground="#ECEFF4", background="#2E3440"
        )
        username_label.pack()
        self.signup_username_entry = ttk.Entry(self.root, width=30)
        self.signup_username_entry.pack(pady=5)

        # Password
        password_label = ttk.Label(
            self.root, text="Password:", foreground="#ECEFF4", background="#2E3440"
        )
        password_label.pack()
        self.signup_password_entry = ttk.Entry(self.root, width=30, show="*")
        self.signup_password_entry.pack(pady=5)

        # Confirm Password
        confirm_password_label = ttk.Label(
            self.root,
            text="Confirm Password:",
            foreground="#ECEFF4",
            background="#2E3440",
        )
        confirm_password_label.pack()
        self.confirm_password_entry = ttk.Entry(self.root, width=30, show="*")
        self.confirm_password_entry.pack(pady=5)

        # Signup Button
        signup_button = ttk.Button(
            self.root, text="Sign Up", command=self.signup, style="Accent.TButton"
        )
        signup_button.pack(pady=10)

        # Login Link
        login_label = ttk.Label(
            self.root,
            text="Already have an account? Login",
            cursor="hand2",
            foreground="#81A1C1",
            background="#2E3440",
        )
        login_label.pack(pady=5)
        login_label.bind("<Button-1>", lambda e: self.show_login_page())

    def show_password_page(self):
        self.clear_window()
        self.root.geometry("800x500")

        # Title
        title_label = ttk.Label(
            self.root,
            text="Saved Passwords",
            font=("Helvetica", 20, "bold"),
            foreground="#ECEFF4",
            background="#2E3440",
        )
        title_label.pack(pady=20)

        # Treeview to display passwords
        columns = ("Website", "Username", "Password")
        self.tree = ttk.Treeview(
            self.root, columns=columns, show="headings", style="Custom.Treeview"
        )
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Load passwords from the encrypted file
        self.passwords = load_passwords(self.key, self.current_user)
        self.refresh_password_list()

        # Hide/Show Password Button
        self.hide_password = True
        toggle_password_button = ttk.Button(
            self.root,
            text="Show Passwords",
            command=self.toggle_password_visibility,
            style="Accent.TButton",
        )
        toggle_password_button.pack(pady=10)

        # Add Password Button
        add_password_button = ttk.Button(
            self.root,
            text="Add Password",
            command=self.show_add_password_page,
            style="Accent.TButton",
        )
        add_password_button.pack(pady=10)

        # Logout Button
        logout_button = ttk.Button(
            self.root, text="Logout", command=self.logout, style="Accent.TButton"
        )
        logout_button.pack(pady=10)

    def show_add_password_page(self):
        self.clear_window()
        self.root.geometry("400x300")

        # Title
        title_label = ttk.Label(
            self.root,
            text="Add Password",
            font=("Helvetica", 20, "bold"),
            foreground="#ECEFF4",
            background="#2E3440",
        )
        title_label.pack(pady=20)

        # Website
        website_label = ttk.Label(
            self.root, text="Website:", foreground="#ECEFF4", background="#2E3440"
        )
        website_label.pack()
        self.website_entry = ttk.Entry(self.root, width=30)
        self.website_entry.pack(pady=5)

        # Username
        username_label = ttk.Label(
            self.root, text="Username:", foreground="#ECEFF4", background="#2E3440"
        )
        username_label.pack()
        self.new_username_entry = ttk.Entry(self.root, width=30)
        self.new_username_entry.pack(pady=5)

        # Password
        password_label = ttk.Label(
            self.root, text="Password:", foreground="#ECEFF4", background="#2E3440"
        )
        password_label.pack()
        self.new_password_entry = ttk.Entry(self.root, width=30, show="*")
        self.new_password_entry.pack(pady=5)

        # Add Button
        add_button = ttk.Button(
            self.root, text="Add", command=self.add_password, style="Accent.TButton"
        )
        add_button.pack(pady=10)

        # Back Button
        back_button = ttk.Button(
            self.root,
            text="Back",
            command=self.show_password_page,
            style="Accent.TButton",
        )
        back_button.pack(pady=10)

    def refresh_password_list(self):
        self.tree.delete(*self.tree.get_children())
        for website, username, password in self.passwords:
            displayed_password = (
                password if not self.hide_password else "*" * len(password)
            )
            self.tree.insert("", "end", values=(website, username, displayed_password))

    def toggle_password_visibility(self):
        self.hide_password = not self.hide_password
        self.refresh_password_list()

    def add_password(self):
        website = self.website_entry.get()
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()

        if not website or not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        self.passwords.append((website, username, password))
        save_passwords(
            self.passwords, self.key, self.current_user
        )  # Save passwords to the encrypted file
        messagebox.showinfo("Success", "Password added successfully!")
        self.show_password_page()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.users and self.users[username] == password:
            self.current_user = username
            self.show_password_page()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def signup(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if password != confirm_password:
            messagebox.showerror("Signup Failed", "Passwords do not match")
            return

        if username in self.users:
            messagebox.showerror("Signup Failed", "Username already exists")
            return

        self.users[username] = password
        save_users(self.users, self.key)
        messagebox.showinfo("Signup Successful", "Account created successfully")
        self.show_login_page()

    def logout(self):
        self.current_user = None
        self.show_login_page()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()

    # Custom Styles
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure(
        "Accent.TButton",
        font=("Helvetica", 12),
        background="#81A1C1",
        foreground="#2E3440",
    )
    style.configure(
        "Custom.Treeview",
        font=("Helvetica", 12),
        background="#3B4252",
        foreground="#ECEFF4",
        fieldbackground="#3B4252",
    )
    style.map("Custom.Treeview", background=[("selected", "#81A1C1")])

    app = PasswordManager(root)
    root.mainloop()
