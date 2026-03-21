## Running the Project with Cloud SQL

1. Install Cloud SQL Auth Proxy
2. Obtain service account key (provided separately)
3. Run:

export GOOGLE_APPLICATION_CREDENTIALS=key.json
./cloud-sql-proxy <INSTANCE_CONNECTION_NAME>

4. Start Django:

python manage.py runserver