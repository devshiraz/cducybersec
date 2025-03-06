# CDU Cybersecurity Club

This project is a GUI application for managing membership in the CDU Cybersecurity Club. It allows users to register as members, view registered members, and securely exit the application.

## Features

- **User Registration**: Users can register by providing their student ID, name, and email.
- **Email Validation**: The application validates the email format before allowing submission.
- **Welcome Messages**: After registration, users receive a cybersecurity-themed welcome message.
- **View Members**: Admins can view a list of registered members.
- **Secure Exit**: The application can only be closed by entering a security code.

## Requirements

- Python 3.x
- Tkinter
- SQLite3
- Pillow (PIL)

## Installation

1. Clone the repository
2. Install the required packages

## Usage
1. Run the application:
   
   ```sh
   python cyberclub.py

2. The application will open in fullscreen mode with a welcome screen.
3. Click "Become a Member" to open the registration form.
4. Fill in the student ID, name, and email fields. The submit button will be enabled once all fields are correctly filled.
5. Click "Submit" to register. A welcome message will be displayed.
6. To view registered members, press Ctrl+Shift+V.
7. To securely exit the application, press Ctrl+Shift+X and enter the security code (shiraz).
