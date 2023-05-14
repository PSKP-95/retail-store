# API Gateway

Nginx based API Gateway for Retail App

## Docker

### Build

```
sudo docker build --force-rm -f Dockerfile -t api-gateway:0.0.3-ssl .
sudo docker push 738241981240.dkr.ecr.ap-south-1.amazonaws.com/api-gateway:0.0.3-ssl
sudo docker push 738241981240.dkr.ecr.ap-south-1.amazonaws.com/api-gateway:0.0.3-ssl
```

### Run

```
sudo docker run --network host -d -v /etc/letsencrypt/:/etc/letsencrypt/ 738241981240.dkr.ecr.ap-south-1.amazonaws.com/api-gateway:0.0.3-ssl
```
