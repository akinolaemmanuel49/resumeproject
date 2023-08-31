# ResumeProject

Welcome to the **ResumeProject** GitHub repository! This project is designed to help users create and manage their resumes online. It utilizes Django as the backend framework and Bootstrap 5 for the user interface. The app provides features such as user authentication, resume creation forms, and the ability to convert resumes to PDF format using wkhtmltopdf.

## Features

- **User Authentication**: Users can register and log in securely to create and manage their resumes.

- **Bootstrap 5 UI**: The user interface is designed using Bootstrap 5, ensuring a responsive and modern design.

- **Resume Creation**: Users can fill in details about their education, work experience, skills, and more using interactive forms.

- **PDF Conversion**: Resumes can be converted to PDF format using the wkhtmltopdf tool, providing a downloadable and printable version.

## Requirements

Make sure you have the following dependencies installed before running the app:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains the necessary Python packages and versions.

## Getting Started

Follow these steps to get the project up and running on your local machine:

1. Clone this repository:

```bash
git clone https://github.com/akinolaemmanuel49/resumeproject.git
cd resumeproject
```

2. Create a virtual environment (recommended) and activate it:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the project dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations to set up the database:

```bash
python manage.py migrate
```

5. Create a superuser account for admin access:

```bash
python manage.py createsuperuser
```

6. Add the .env file and place it in the root directory, you can use the example.env file for guidance or set the environment variables:
```bash
SECRET_KEY="secret-key"
EMAIL_HOST="smtp.provider.com"
EMAIL_HOST_USER="example.mail.com"
EMAIL_HOST_PASSWORD="password"
EMAIL_PORT= 587
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL="resumebuilder@resumebuilder.com"
```

7. Run the development server:

```bash
python manage.py runserver
```

8. Open a web browser and navigate to `http://127.0.0.1:8000` to access the app.

## Running Tests

This repository includes test cases to ensure the functionality of the app. To run the tests, use the following command:

```bash
python manage.py test
```

This command will execute the test suite and provide you with information about the tests' success.

Feel free to explore the app's features, create resumes, and generate PDFs of your resumes!

If you encounter any issues or have questions, please don't hesitate to open an issue on this repository. Happy coding!