## Running the Project with Cloud SQL

1. Install Cloud SQL Auth Proxy - included in zip nothing needs to be donej
2. Obtain service account key (provided separately)
3. Run:
    run this command in powershell (windows). it will run a proxy that will allow you to run the app on local host, and it will proxy to the
    public ip. This is done for security. I was getting weird traffic leaving public access open and it was costing me money:
    .\cloud-sql-proxy.exe --credentials-file="key.json" --port=3306 high-balancer-486900-c3
4. Start Django:

python manage.py runserver