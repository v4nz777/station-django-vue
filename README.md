# station-django-vue

by: v4nz777

A web-based general application built using Django and Vue.js
to help and automate most task in radio station

## Backend (WEB API)

- Built using Django and the Django REST framework
- Utilizes a PostgreSQL database to store user data
- Includes functionality for user authentication and authorization using JWT tokens
- Using websocket to update see activites and updates in real time.

## Frontend (DEPLOYMENT)

- Deployed with NGINX
- SSL/TLS Enabled at `192.168.1.77:443` using https for secure connection.
  

## Frontend (PRODUCTION)

- Built using Vue.js and the Pinia library for state management
- Communicates with the backend API to retrieve and manipulate data
- Includes functionality for user authentication and authorization

## Getting Started

1. Clone the repository:
`git clone https://github.com/v4nz777/station-django-vue.git`

2. SSL Certificates are made for IP address `192.168.1.77` so make sure that your machine are using IPV4 192.168.1.77 . 

3. If you are using 192.168.1.77 already, skip this step, otherwise create a new SSL certificate using the steps below:
   Making SSL Certificate:
    - navigate to folder `ssl`
    - Install openSSL in your machine: `https://www.ibm.com/docs/en/ts4500-tape-library?topic=openssl-installing`
    - Create new key: `openssl req -x509 -newkey rsa:4096 -keyout rootCA.key -out rootCA.crt -days 99999 -config ssl.conf -nodes`
   
5. Make sure that your IP is DHCP reserved or STATIC.

6. Create `config.py` inside `/backend/backend/` then configure the following settings inside `config` file:
    - `SECRET_KEY`
    - `DATABASES`
    - `CHANNEL_LAYERS`
    - `SERVE_AT` default is `192.168.1.77`
      
7. Build using Docker:
   `docker-compose build`

8. Run.
   `docker-compose up`

5

Note: 
- Make sure that you have node js installed in your system to run the frontend.
- You can also run the frontend using yarn by replacing `npm` with `yarn`

The application should now be running at `http://localhost:8000` and the frontend should be running at `http://localhost:5173`.

