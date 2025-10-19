# Chesso server

## Run in local

```bash
uvicorn main:app --reload
```

## Run in production

Note that this requires to have the [mazerfaker_proxy](https://github.com/macsimbodnar/mazerfaker_proxy) running.
It will handle https and reverse-proxy

```bash
# Start
docker compose up --build -d

# Stop
docker compose down

# Monitor logs
docker compose logs --follow 

# OR start attached to the shell
docker compose up --build 
```

## Cleanup dockers for free space on server

```bash
docker rm -vf $(docker ps -aq)
docker rmi -f $(docker images -aq)
```

## TODO List

* Sounds
* Timer
* Load fen string

### NOTE

[Lichess board configuration](https://github.com/lichess-org/chessground/blob/master/src/config.ts)
