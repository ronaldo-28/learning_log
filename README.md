# learning_log

I have written a a web app called Learning Log using Django, Bootstrap and Sqlite. Learning Log is a web app that allows users to log the topics they’re interested in and make journal entries as they learn about each topic. The web app has a home page that describes the site and invites users to either register or log in. Once logged in, a user can create new topics, add new entries, and read and edit existing entries. The web app also has some features that 
enhance its functionality and security, such as:


Adding an ellipsis to the entry title only if the entry is longer than 50 characters.

Checking that the user associated with a topic matches the currently logged-in user before displaying or editing the topic or its entries.

Applying Bootstrap’s styles to the form-based pages for a better user interface.

Giving users the option of making a topic public so that other users can view it.

# Running the Django Project Locally on Windows

Follow these steps to set up and run the Django project.

## 1. Create a Virtual Environment and Activate It

Create a new virtual environment called `ll_env` by running:

```bash
python -m venv ll_env

```

Activate the virtual environment by running:

windows powershell:
```powershell
.\ll_env\Scripts\Activate.ps1
```

linux:
```bash
source ll_env/bin/activate
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Apply Database Migrations

```bash
python manage.py migrate
```

## 4. Run the Django Development Server

```bash
python manage.py runserver
```

## 5. Deactivate the Virtual Environment

```bash
deactivate
```

## 6. Create a Superuser

```bash
python manage.py createsuperuser
```
