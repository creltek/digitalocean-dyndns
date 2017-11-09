# Build Image

```
$ docker build -t digitalocean-dyndns ./
```

# Run Container

```
$ docker run -d --name digitalocean-dyndns -e HOST=home -e DOMAIN=example.com -e KEY=$(access_token) digitalocean-dyndns
```