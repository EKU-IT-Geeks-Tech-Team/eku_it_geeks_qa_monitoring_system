docker stop geeksqa
docker build -t geeks/qa .
docker run -d --restart unless-stopped -p 80:8000 -v /root/eku_it_geeks_qa_monitoring_system/db.sqlite3:/usr/src/app/db.sqlite3 --name geeksqa geeks/qa
