
Install Docker and Docker Compose:

Go to this link and follow the instalation steps using wsl2:
https://docs.docker.com/desktop/install/windows-install/


Clone the project and "cd" into it:
```bash
git clone https://git.luminess.eu/luminess-indus-toolkit/training/internship2024/microservices-course/microservices.git

cd microservices/
```



Run the project:

Depending on your instalation, the "docker compose" command could also be "docker-compose".
Try them both and use the own that works for you.

```bash
docker compose up -d --build
```


Minio:
From admin interface; set public policy on the bucket



Upload interface: 80
Storage service: 8000
Displaying service: 5000
Minio: 9000 for API; 9001 for GUI
Postgresql: 5432 


Useful commands:

docker compose logs
docker compose logs <service_name>
docker compose up
docker compose down
docker compose up --build -d --remove-orphans

