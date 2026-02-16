#!/bin/bash
base_python_interpreter="/home/www/.python/bin/python3.9"
project_domain=""
project_path=`pwd`
base_folder=`pwd | xargs basename`

mv nginx/site.conf nginx/$base_folder.conf
mv systemd/gunicorn.service systemd/$base_folder-gunicorn.service

#read -p "Python interpreter: " base_python_interpreter
read -p "Your domain without protocol (or IP): " project_domain
`$base_python_interpreter -m venv env`
source env/bin/activate
pip install -U pip
pip install -r requirements.txt

sed -i "s~dbms_template_path~$project_path~g" nginx/$base_folder.conf systemd/$base_folder-gunicorn.service
sed -i "s~base_folder~$base_folder~g" nginx/$base_folder.conf systemd/$base_folder-gunicorn.service
sed -i "s~dbms_template_domain~$project_domain~g" nginx/$base_folder.conf src/config/settings.py
#sed -i "s~base_folder~$base_folder~g" nginx/$base_folder.conf src/config/settings.py

sudo ln -s $project_path/nginx/$base_folder.conf /etc/nginx/sites-enabled/
sudo ln -s $project_path/systemd/$base_folder-gunicorn.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl start $base_folder-gunicorn.service
sudo systemctl enable $base_folder-gunicorn.service
sudo nginx -s reload
