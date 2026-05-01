# BLOG API -HW4 

# RUNNING THE PROJECT 

FIRSTLY 
make the 
 
 ```bash 
 docker compose up --build 
```


The app is available only through nginx: 
so 
`` `text
http://localhost/
``

The django `web` container listnen the port `8000` only inside the Docker Compose network. 


## Checking

```bash
curl -I http://localhost/admin/login/
```
expected 200 

```bash
curl http://localhost/api/posts/

```
expected json file with data 


or you can run if the nginx is give you  502 error 
like the
```bash
curl -I http://localhost/api/posts/
```
then you get the 200 


# The last thing is the Websocket

To check it we should hav eaccount like register/login in the app

```bash
curl -s -X POST http://localhost/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"hw4@example.com","first_name":"HW","last_name":"User","password":"password123","password_confirm":"password123"}'
```



Use the returned access token as `<jwt>`.

Create or choose an existing post slug, then connect:

```bash
wscat -c "ws://localhost/ws/posts/<existing-slug>/comments/?token=<jwt>"
```

Expected: WebSocket handshake returns `101 Switching Protocols`.

In another terminal, post a comment:

```bash
curl -X POST http://localhost/api/posts/<existing-slug>/comments/ \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{"body":"hello through nginx websocket"}'
```

Expected: the WebSocket terminal receives the new comment message.


## FInally the homework is done