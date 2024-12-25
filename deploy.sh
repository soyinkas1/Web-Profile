# Save this script on your PythonAnywhere account, e.g., `deploy.sh`

#!/bin/bash
cd /home/shosowoolu/Web-Profile
git pull origin main
source /home/shosowoolu/.virtualenvs/my-virtualenv/bin/activate
pip install -r requirements.txt
# Restart the web app (replace `yourusername` and `yourwebapp` with your actual details)
pa_reload_webapp.py www.soyinkasowoolu.com
