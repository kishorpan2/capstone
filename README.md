# Expense Tracker

Expense tracker is a Python CRUD Application and visualization in chart .

### Installation

Django
VS Code

python3 -m venv project-name

### Activate python environment 
source {{project-name}}/bin/activate 

### Deactivate python environment
deactivate

Install Django
python3 -m pip install django

### Create a django project
django-admin startproject capstone_project

### Create an app inside the peoject 
python3 manage.py main

### Command to run Django server
python3 manage.py runserver
### Usage

visually inspect the expense

### create expense
enter expense details in "Add an expense page"

### edit expense
edit expense details in "Edit an expense page"

### delete expense
delete expense 

### Summary
summary page to find all the expense summary in one place

# Deploymenet steps:
Django deployment in EC2

Login in to AWS Console

Go to ec2 by searching Ec2 in the search box or selecting EC2 under services

Select an Ubuntu AMI and create an instance of Ubuntu VM
After the server is up and running, ssh into the EC2 VM

Inside the project directory in your local machine,run the command to create requirements file and gitignore files

python3 -m pip freeze > requirements.txt
touch .gitignore to create a gitignore file to filter files to github

Inside the .gitignore file add this code:

.vscode
env/
venv/
__pycache__/
.vscode/
Db.sqlite3

(git add, commit, push) ACP to github
Find the access key and chmod 400 .pem key
Ssh into the the instance using the following command

 ssh -i "yourpemkey.pem" ubuntu@ec2-3-94-59-216.compute-1.amazonaws.com
 
After you ssh into the instance, run the following command to update apt-get:

Update your machine with current settings 
```
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev nginx curl
```
Clone your git repo by using the following command
```
git clone {{url for git repo where the application lives}}
```
Create virtual environment inside the instance by:
```
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
mkdir ~/myprojectdir
cd ~/myprojectdir
virtualenv myprojectenv
source myprojectenv/bin/activate
```
Install all the necessary requirements using the following commands:
```
pip install django==4.0
pip install bcrypt to install bcrypt
pip install gunicorn to install gunicorn
```
Cd into the project name
```
sudo vim install settings.py to modify the file
```
Change the following lines in settings.py:
```
import os
DEBUG = False
ALLOWED_HOSTS = ['{{yourEC2.public.ip}}'] # keep the quotes!
STATIC_ROOT = os.path.join(BASE_DIR, "static/") # add this line at the bottom;

Save and quit these files
```
Cd .. to go back to parent directory

Gather all of the static files in your project into one location by running the following command
```
python manage.py collectstatic # type yes
```
Let's first test Gunicorn by directing it to our Django project's wsgi.py file, which is the entry point of the application by running the following command:
```
gunicorn {{project_name}}.wsgi
```
Exit the process by typing ctrl-c .

```
sudo vim /etc/systemd/system/gunicorn.socket
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```
sudo vim /etc/systemd/system/gunicorn.service
```
 [Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/app/capstone
ExecStart=/home/ubuntu/app/env/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          capstone_project.wsgi:application

[Install]
WantedBy=multi-user.target       
```
Now that our service file has been created, we can enable it so it starts on boot.
```
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl status gunicorn
```
Then ctrlC to stop the process
```
sudo journalctl -u gunicorn.socket
```
the following command is a very useful command, If you get an HTML for your index page then you are on the right path
```
curl --unix-socket /run/gunicorn.sock localhost
```
```
file /run/gunicorn.sock
```
Now, configure the NGINX web server 

sudo vim /etc/nginx/sites-available/{{projectName}}
Configure the file with the following info inside the file
```
server {
listen 80;
Server_name{{your public ip address}};
location = /favicon.ico { access_log off; log_not_found off; }
location /static/ {
root /home/ubuntu/capstone;
}
location / {
include proxy_params;
proxy_pass http://unix:/home/ubuntu/capstone/capstone_project.sock;
}
}
Save and quit the file using esc :wq
```
Now we're going to create a link to this file to let NGINX know what settings to use.
```
sudo ln -s /etc/nginx/sites-available/capstone_project /etc/nginx/sites-enabled
```
CHECK: Make sure the link was successful. If not successful, double and triple check the file
```
sudo nginx -t
```
Now that we have our custom configuration, we will remove the Nginx default site
```
sudo rm /etc/nginx/sites-enabled/default
```
All that is left to do is restart our NGINX server with our updated settings.
```
sudo service nginx restart
```
Now try to see if you can access your application in the following link:
```
http://{{your public ec2 ip}}

```
## Contributors:
**Kishor Pandey**
**Pemba Sherpa**

## License
[MIT](https://choosealicense.com/licenses/mit/)

# References
https://docs.djangoproject.com/en/4.0/
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04