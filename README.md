
**Name:          Joseph Mania<br>
Reg.:          J17/0835/2019<br>
Supervisor:    Madam Winnie S W Wachira<br>
Academic year: 2022-2023**<br>

# EmployNanny
A web Application that allows nannies to find jobs and employers can find good talent for their housework.
This is a job portal platform for connecting nannies with their respective employers.
https://employnannies.onrender.com/

# Installation
Clone the EmployNanny repository from GitHub:<br>
bash
Copy code<br/>
`git clone https://github.com/maniamartial/EmployNanny.git`

Change into the project directory:
Copy code<br/>
`cd EmployNanny`

## (Optional) Set up a virtual environment (recommended):

### On macOS and Linux
`python3 -m venv env`

### On Windows
`python -m venv env`

## Activate the virtual environment (skip this step if you're not using a virtual environment):
### On macOS and Linux
`source env/bin/activate `

### On Windows
`env\Scripts\activate`

## Install the required Python packages
`pip install -r requirements.txt`

## Configuration
The project relies on some environment variables for configuration. Create a .env file in the project's root directory and add the following key-value pairs:<br>
`SECRET_KEY=your_secret_key_here
DEBUG=True`
<br>
Replace your_secret_key_here with a random string Django will use as the project's secret key. Remember to keep your actual secret key private and never share it publicly.

## Database Setup
EmployNanny uses Django's default database SQLite for simplicity. <br>
Install PostgreSQL and create database called Employnany<br>
Apply migrations to create the database schema:<br>
`python manage.py migrate`<br>

## Create a superuser account to access the Django admin panel:
<br>
`python manage.py createsuperuser`<br>
Follow the prompts to set up your superuser account credentials.<br>

## Running the Development Server
Now that everything is set up, you can start the Django development server:<br>
`python manage.py runserver`<br>
The server will run at http://127.0.0.1:8000/. You can access the application by visiting this URL in your web browser.<br>

## Django Admin Panel
To access the Django admin panel and manage the application data, follow these steps:<br>

**Run the development server if it's not already running:**<br/>
`python manage.py runserver`<br>
Open your web browser and go to http://127.0.0.1:8000/admin/.<br>

Log in using the superuser account credentials you created earlier.
