# Cipher Vault - Password Manager with Encryption

This is a simple yet secure password manager application built using Python and the Tkinter library. It allows users to securely store and manage their passwords with encryption, ensuring their sensitive data remains safe.

### Features:
- User Authentication (Login/Signup)
- Add, view, and manage passwords
- Password encryption using the `cryptography` library (Fernet)
- Store passwords securely in an encrypted file
- View or hide passwords in the password list

---

## Requirements

To run this application, you'll need to install the following dependencies:

- Python 3.x
- `cryptography` library
- `tkinter` (usually pre-installed with Python)

You can install the required libraries using:

```bash
pip install cryptography
```

---

## File Structure

```
├── data/
│   ├── secret.key      # Encryption key used to encrypt/decrypt passwords
│   ├── users.enc       # Encrypted user data
│   └── <username>.enc  # Encrypted password storage for each user
├── main.py             # Main Python file containing the app logic
├── README.md           # Project documentation
```

---

## Usage

1. **Run the program**: Simply run the `main.py` file to start the password manager.

   ```bash
   python main.py
   ```

2. **Login / Sign Up**:
   - If you don't have an account, click "Don't have an account? Sign up" to create a new user.
   - If you already have an account, enter your username and password to log in.

3. **Add Passwords**:
   - Once logged in, you can add websites, usernames, and passwords to your password list by clicking the "Add Password" button.
   
4. **View / Hide Passwords**:
   - The "Show Passwords" button allows you to toggle visibility of the saved passwords.

5. **Logout**: Logout from the current session by clicking the "Logout" button.

---

## Encryption

This application uses the `cryptography` library to encrypt and decrypt passwords. Each user's passwords are stored in a unique encrypted file, ensuring that the passwords are safe. The encryption key is stored in the `secret.key` file, which is used for encrypting and decrypting data.

- **Generate Key**: If the `secret.key` file does not exist, a new key is generated automatically.
- **Encrypt Data**: Passwords and other sensitive information (such as usernames and website URLs) are encrypted using the generated key.
- **Decrypt Data**: Encrypted data can be decrypted using the same key when needed.

