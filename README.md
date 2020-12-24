# Timetracker/Timesheet generator


A basic version of script that fetches data from Hubstaff using Hubstaff API V1 and generates a timesheet of any organization their onging project, active members and time spent on the projects.


Built by  [Aakash Shrestha](https://github.com/aakashres)

---
# Installation
This project is based on Python==3.6 and a some libraries metioned in requirements.txt

# Setup Project
1. Locally
    1. Make sure python3.8 is installed. Its better to do all these steps in a virtualevironment.
    2. Navigate to project folder
    3.  Run ```pip install -r requirements.txt```. This should install all dependencies
    4.  Create ```.env``` file inside /app (Contents example is listed below)
    5.   Run ```python app/main.py```
    6.   Output HTML is located in ```app/output/timesheet.html```
    7.   Logs are located in ```app/logs/app.logs```
2. Docker
    1. Navigate to project folder
    2. Create ```.env``` file inside /app (Contents example is listed below)
    3. docker build -t <image_name> .
    4. ```docker run -v $PWD/app:/app -it <image_name>```
    5.  Output HTML is located in ```app/output/timesheet.html```
    6.  Logs are located in ```app/logs/app.logs```

# .env file setup example
Create ```.env``` file inside ```/app``` (Contents example is listed below)
```
HUBSTAFF_EMAIL=******@****.***
HUBSTAFF_PASSWORD=***********
HUBSTAFF_APP_TOKEN=*********************
```
