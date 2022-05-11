# Student Learning Quality Monitoring System

## Environments Setup

```
conda create -n django python=3.8
conda activate django
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## Deploying

```
python manage.py runserver
```
 
Open [this link](http://127.0.0.1:8000/login/) for login entry view for the whole website.

Open [this link](http://127.0.0.1:8000/) for look up three data tables including username and passwords.