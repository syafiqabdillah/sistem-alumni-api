# Sistem Alumni - API
Author: Syafiq Abdillah Umarghanis abdillah.syafiq@gmail.com
## System Requirements 
- Git
- Python 3.x
## Database Setup
1. Import the sql dump sent via email to the existing MySQL server 
## Production Setup 
1. Clone the repository
```bash
$ git clone https://github.com/syafiqabdillah/sistem-alumni-api.git
```
2. Install Python's virtual environment library 
```bash
$ python -m pip install virtualenv 
```
3. Change current directory to `sistem-alumni-api`
```bash
$ cd sistem-alumni-api
```
4. Create a virtual environment 
```bash
$ python -m virtualenv venv
```
5. Activate the virtual environment 
```bash
$ source venv/bin/activate 
```
6. Install all dependencies 
```bash
(venv) $ pip install -r requirements.txt
```
7. Put the `.env` file sent via email in the `sistem-alumni-api` directory. It contains all variables needed for the app to run properly. Change its content based on real system & database configuration.
```
DB_HOST=localhost
DB_NAME=sistem_alumni
DB_USER=user123
DB_PASS=pass123
PORT=8000
WEB_URL=sistem-alumni-asysyaamil-web.herokuapp.com
SECRET=secret123
```
8. Run the server 
```bash
(venv) $ python main.py
```