.\venv\Scripts\Activate
pip install -r requirements.txt

Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd "C:\path\to\proxy"; .\cloud-sql-proxy.exe --credentials-file="key.json" --port=3306 high-balancer-486900-c3:us-central1:deliveries-instance'

python manage.py runserver