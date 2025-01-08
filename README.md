# Email Bot

This bot is a small web application intended to allow you to send emails based on a preconfigured template. 
The core functionality of the website has 3 pages:
- Homepage - Displays the signed in user and some basic stats
- Upload Page - Allows user to upload a spreadsheet and send emails for each row in the spreadsheet. (Specifics of format for spreadsheet to be discussed in depth below)
- Responses Page - Allows user to see whether or not they have received an email in response for each email they have sent out

## Getting started
### Frontend
The repo has a frontend written as a React app using Vite to bootstrap the build. 
If you are building the repo locally for the first time, you should just do the following:
- cd email_bot_frontend
- npm install (only do this the first time you build the repo)
- npm run dev

### Backend
The backend is written in Python and uses a library called FastAPI to expose
the endpoints to the frontend. 
If you are building the repo locally for the first time, please do the following:
1. Please make sure you have python installed on your machine. 
   1. You can do this by opening up a terminal window (mac) or command prompt (windows) and typing the following:
   2. python --version (you may have to write python3 --version)
   3. If you see that python (or python3) is not a recognized command, please watch a tutorial on installing python
2. You SHOULD create a virtual environment for this project. Please do this by doing the following:
   1. cd email_bot_backend
   2. python -m venv venv
   3. If on mac, activate the environment by typing the following in terminal:
      1. source ./venv/bin/activate
   4. If on windows, activate instead by typing the following in command prompt:
      1. source venv/Scripts/activate

To install the projects required python libraries, please first make sure you are in the directory called
email_bot_backened. If you are in the email_bot directory, change into the email_bot_backend directory by running the following command in terminal / Command Prompt
- cd email_bot_backend

Once in the email_bot_backend directory, ensure your venv is activate (see above) and then run this command to install the required libraries
- pip install -r requirements.txt

Now you should be ready to start the backend server running locally on your machine.
You do this by running the following command:
- uvicorn main:app --reload



## Template and Configurations

### Email Template
The email template is not currently configurable from the frontend. 

To edit the subject or template, you can go to template.py. The template for the email is currently defined as follows in template.py

```python
    subject = f"Reaching out about {property_name}"

    template = (f"Hi {first_name},"
                f"Hope you’re doing well."
                f"It’s Eric Schwartz from BASE Realty Group."
                f"A client of mine came across your asset, {property_name}."
                f"They asked me to get in touch with you to see if you would entertain an offer on it."
                f"I'm happy to discuss further at your earliest convenience."
    )
```

### Upload Spreadsheet Format
The current format for an uploaded spreadsheet is as follows:

![img.png](spreadsheet_example.png)

The order of the columns does NOT matter but the following columns are required
and if they are omitted will cause an error:
1. Property Name (row cannot be blank)
2. At least 1 column of "Name" (row cannot be blank)
3. At least 1 column of "Email" (row cannot be blank)
4. Property Address (you CAN leave the row blank but the column must exist)

