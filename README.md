# :computer: BRblog - Post your blog with extended functions!

### Technologies Stack
- Django
- SQLLite(You can change it to Postgres or e.g on your own)
- HTML / CSS
- AJAX

### Developer Staff
- [dynamitebilol](https://github.com/dynamitebilol)
- Templates for frontend were taken from freecodecamp-NewsFlash

### Website Features
- Browse and search for posts
- Views, likes, comments
- Likes without refreshing page via AJAX
- Sign up and log in into account
- Login via Google (Oauth)
- Create / Edit / Delete your posts
- Comment other's projects



### Preview
![Preview](https://i.ibb.co/VmrndYg/BR-Blog-3.png)
![Preview](https://i.ibb.co/qrV7wD2/BR-Blog-2.png)
![Preview](https://i.ibb.co/RbW27YG/BR-Blog.png)

### Run it yourself
```sh
git clone https://github.com/dynamitebilol/brblog.git
cd finddev
pip install - r requirements.txt
```

Go to the `settings.py` and change this lines up to your PostgreSQL account
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'brblog',
        'HOST': 'localhost',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': ENV['DB_PASS']
    }
}
```
Then run the migrations:
```sh
python manage.py migrate
```


Then you can run it
```sh
python manage.py runserver
```
