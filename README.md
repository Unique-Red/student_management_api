# Student Management API

Student Management API as the name implies, it is used manage students data (their basic informations, course and score)

## Features
- Endpoints for creating, reading, updating, and deleting students.
- Registration of course by students.
- View the number of students taking a course.
- Retrieving all the students, course and the ones that registered a particular course.
- GPA calculation.
- JWT Authentication and authorization.

<hr>

## Built with:
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

<hr>

## Get a copy
It is believed that you have python installed already. Open CMD or terminal
1. Clone this repo
```sh
git clone https://github.com/Unique-Red/student_management_api.git
```
2. Open the directory
```sh
cd student_management_api
```
3. Create Virtual Environment
```sh
python -m venv <your-venv-name>
```
4. Activate virtual environment on CMD or Powershell
```sh
<your-venv-name>\Scripts\activate.bat
```
On gitbash terminal
```sh
source <your-venv-name>/Scripts/activate.csh
```
5. Install project packages
```sh
pip install -r requirements.txt
```
6. Set environment variable
```sh
set FLASK_APP=app.py
```
On gitbash terminal
```sh
export FLASK_APP=run.py
```
7. Create database
```sh
flask shell
```
```sh
db.create_all()
quit()
```
8. Run program
```sh
python app.py
```
<hr>

![Render](https://img.shields.io/badge/Render-%46E3B7.svg?style=for-the-badge&logo=render&logoColor=white)
<br/>
Live link: <a href="https://stma.onrender.com/">STMA</a>