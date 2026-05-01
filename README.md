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
curl - I http://localhost/admin/login/
```
