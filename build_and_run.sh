docker build -t geeks/qa .
docker run --rm -d -p 8000:8000 --name geeksqa geeks/qa