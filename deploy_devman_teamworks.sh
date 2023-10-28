#!/bin/bash
cd /opt/devman_teamworks
git pull
source ./env/bin/activate
pip install -r requirements.txt
python3 ./manage.py collectstatic --noinput
echo "Checking for the need for makemigrations"
python3 ./manage.py makemigrations --dry-run --check
python3 ./manage.py migrate --noinput
systemctl reload-or-restart devman_teamworks.service
systemctl reload-or-restart nginx.service
sleep 3
DEVMAN_TEAMWORKS_STATUS="$(systemctl is-active devman_teamworks.service)"
NGINX_STATUS="$(systemctl is-active nginx.service)"
if [ "${DEVMAN_TEAMWORKS_STATUS}" != "active" ]; then
    echo "devman_teamworks.service restart error"
    exit 0
fi
echo "the devman_teamworks.service is working"
if [ "${NGINX_STATUS}" != "active" ]; then
    echo "nginx.service restart error"
    exit 0
fi
echo "the nginx.service is working"

echo "Updated successfully."
