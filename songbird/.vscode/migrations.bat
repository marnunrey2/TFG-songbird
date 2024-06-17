@echo off
echo Going back one directory...
cd ..

echo Installing requirements...
pip install -r requirements.txt

echo Running "python manage.py makemigrations"...
python manage.py makemigrations

echo Running "python manage.py migrate"...
python manage.py migrate

echo Running "python manage.py runserver"...
python manage.py runserver

echo All steps completed successfully.