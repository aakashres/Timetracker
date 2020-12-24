# Timetracker/Timesheet generator

A basic version of the script that fetches data from Hubstaff using Hubstaff API v1 generates a timesheet of any organization, ongoing project, active members, and time spent on the projects. It formats all data, compiles them, and saves them as output HTML. This project is based on Python==3.8, Hubstaff API v1, and some libraries mentioned in ```requirements.txt```.

All necessary tokens and config are saved in the ```.env``` file inside the ```/app``` directory. Make sure that it is present before execution.

# Setup Project
1. Locally
    1. Make sure python3.8 is installed. It is better to carry out all these steps in a virtualevironment.
    2. Navigate to project folder
    3. Run ```pip install -r requirements.txt```. This should install all dependencies
    4. Create ```.env``` file inside ```/app``` (Contents example is listed below)
    5. Run ```python app/main.py```
    6. Output HTML is located in ```app/output/timesheet.html```
    7. Logs are located in ```app/logs/app.logs```
2. Docker
    1. Navigate to project folder
    2. Create ```.env``` file inside ```/app``` (Contents example is listed below)
    3. ```docker build -t <image_name> .```
    4. ```docker run -v $PWD/app:/app -it <image_name>```
    5. Output HTML is located in ```app/output/timesheet.html```
    6. Logs are located in ```app/logs/app.logs```

# .env file setup example
Create ```.env``` file inside ```/app``` (Contents example is listed below)
```
HUBSTAFF_EMAIL=user@example.com
HUBSTAFF_PASSWORD=my_passwrod_goes_here
HUBSTAFF_APP_TOKEN=MYAPITOKENGOESHERE123
```
