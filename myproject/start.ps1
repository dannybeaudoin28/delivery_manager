.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd "proxy"; .\cloud-sql-proxy.exe --credentials-file="key.json" --port=3306 high-balancer-486900-c3:us-central1:deliveries-instance'

python manage.py runserver