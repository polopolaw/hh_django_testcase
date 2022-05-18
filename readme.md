## Installation ##
#### Copy file .env.example to .env and fill your data if it needed.

If you Linux user, use that:
```commandline

move stripe_integration/.env.example stripe_integration/.env
nano stripe_integration/.env
```
#### Activate venv
```commandline
source venv/bin/activate
```
#### Install dependencies
```commandline
pip install -r requirements.txt
```
#### Run migrations, run seeders. Test creds (user:user)
```commandline
python manage.py migrate
python manage.py seeder
python manage.py runserver
```
##Have fun!

