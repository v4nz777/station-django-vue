# station-django-vue

A web-based general application built using Django and Vue.js
to help and automate most task in radio station

## Backend

- Built using Django and the Django REST framework
- Utilizes a PostgreSQL database to store user data and music metadata
- Includes functionality for user authentication and authorization using JWT tokens

## Frontend

- Built using Vue.js and the Pinia library for state management
- Communicates with the backend API to retrieve and manipulate data
- Includes functionality for user authentication and authorization

## Getting Started

1. Clone the repository:
`git clone https://github.com/v4nz777/station-django-vue.git`

2. Install the dependencies:
`pip install -r requirements.txt`

3. Create a `.env` file in the root directory of the project and set the environment variables for the database and JWT secret key.

4. Run migrations:
`python manage.py makemigrations
python manage.py migrate`

5. Run the development server:
`python manage.py runserver`

6. In a separate terminal, navigate to the `frontend-ts` directory and install the dependencies:
`npm install`

7. Run the development server for the frontend:
`npm run dev`


Note: 
- Make sure that you have node js installed in your system to run the frontend.
- You can also run the frontend using yarn by replacing `npm` with `yarn`

The application should now be running at `http://localhost:8000` and the frontend should be running at `http://localhost:5173`.

