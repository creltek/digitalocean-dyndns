#### Build Image

```
$ docker build -t creltek/digitalocean-dyndns ./
```

#### Run Container

```
$ docker run -d --name dyndns creltek/digitalocean-dyndns --host home --domain example.com --key $(access_token)
```