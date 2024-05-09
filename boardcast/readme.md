# run

```shell
sudo docker build -t bserver .
docker run --name bserver -p 8081:8081 -d bserver
```

```shell
sudo docker build --platform linux/amd64 -t bserver .
docker run --name bserver  -p 8000:8000 -d bserver
```