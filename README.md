## Build Image

```
$ docker build -t creltek/digitalocean-dyndns ./
```

## Run Container

```
$ docker run -d --name digitalocean-dyndns -e HOST=home -e DOMAIN=creltek.com -e KEY=$(access_token) creltek/digitalocean-dyndns
```