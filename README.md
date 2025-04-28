# Health Info System

## Project Overview

The Health Info System is a Django-based web application that allows users to manage health programs, client registrations, and enrollments in a seamless and secure environment. The system supports user authentication, program management, and client enrollment functionalities, providing a simple yet effective solution for managing healthcare services.

## Features

- **User Authentication**: Users can sign up, log in, and manage their profiles.
- **Health Programs**: Create, edit, and delete health programs, including details like start and end dates.
- **Client Management**: Register, update, and delete client details, including personal information and enrollment status.
- **Enrollment**: Enroll clients in health programs and track enrollment dates.
- **OTP Verification**: Secure user registration with one-time password (OTP) email verification.
- **Admin Controls**: Only the creator of health programs and clients can edit or delete their respective entries.

## Tech Stack

- **Backend**: Django (Web Framework)
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLite (default for Django)
- **Authentication**: Django's built-in User model and session management
- **Email Service**: Django's `send_mail` function for OTP verification
- **Other Tools**: 
  - `django-cors-headers` for handling cross-origin requests
  - `djangorestframework` for API management (optional)

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Installation

To set up the project on your local machine, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/roran-williams/healthinfo_system.git
    cd healthinfo_system
    ```

2. **Set up a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Create a Superuser**:
    ```bash
    python manage.py createsuperuser
    ```
6. **(Optional) There are two versions of this system, to use the api-first aproach version checkout to api-first-approach**:
    ```bash
    git branch -r
    ```
    ```bash
    git checkout <branch-name>
    ```

7. **Run the Development Server**:
    ```bash
    python manage.py runserver
    ```

The application will be running at `http://localhost:8000`.

## Running the Project

After setting up the environment and running the server, navigate to `http://localhost:8000` to access the application. Use the superuser credentials to log into the admin panel and manage the health programs and client registrations.

## API Endpoints

- **GET /api/clients/**: Retrieve a list of clients.
- **POST /api/clients/**: Register a new client.
- **GET /api/clients/{id}/**: Retrieve client details by ID.
- **POST /api/enroll/**: Enroll a client in a health program.

## Usage

- **User Authentication**: Users need to sign up with their email and password to access the system.
- **Health Program Management**: Only authorized users (those who created the programs) can edit or delete programs.
- **Client Enrollment**: Enroll clients into specific health programs by selecting from the available options.

## Contributing

We welcome contributions! Here’s how you can contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/your-feature-name`)
5. Create a new Pull Request

Please ensure that your contributions follow the project’s coding standards and guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Django Framework for providing a robust web framework.
- Bootstrap for easy and responsive front-end design.
- Django REST Framework for API support.
