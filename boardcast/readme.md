# Build docker and run


```shell
sudo docker build -t bserver .
docker run --name bserver -p 8000:8000 -d bserver
```