## Django - Devsearch

Database - Aiven PostgreSQL

Hosted on - https://django-devsearch-jnbo8kakx-mayank-nagoras-projects.vercel.app/

**01 - Install Virtualenv**

```bash
pip install virtualenv
```
```bash
virtualenv env
```

**02 - Activate Environment**

```bash
source env/Scripts/activate
```

**03 - Deactivate Environment**

```bash
deactivate
```

**04 - Install Django**

```bash
pip install django
```

**05 - Create Project**

```bash
django-admin startproject devsearch .
```

**06 - Start Server**

```bash
python manage.py runserver
```

**07 - Create App**

```bash
django-admin startapp projects
```

**08 - Create Migration from Models**

```bash
python manage.py makemigrations
```

**09 - Executes Migration to DB**

```bash
python manage.py migrate
```

**10 - Create Admin User**

```bash
python manage.py createsuperuser
```

**11 - PostgreSQL database adapter**

```bash
pip install psycopg2-binary
```

**12 - AWS S3 Storage**

```bash
pip install django-storages
pip install boto3
```

**13 - Bundle Static Files**

```bash
python manage.py collectstatic
```

**14 - Pushed code to Github**

```bash
git init
git add .
git commit -m <commit>
git remote <origin>
git push origin master
```

**15 - Deployed on Vercel**

```bash
npm i -g vercel
```







