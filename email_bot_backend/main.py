import datetime
import os.path

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import mimetypes
from pathlib import Path
import io
import uvicorn
import logging
import sys
import pandas as pd
from openpyxl.descriptors import DateTime

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)



from email_functions import search_emails, send_email, signed_in_user
from template import email_template

app = FastAPI()

# Configure CORS
origins = ["http://localhost",
           "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


'''
Want to add a login feature. Currently, I am always selected as the user because of the refresh token in
refresh_token.txt . If I delete it, it takes me through the Auth workflow again but autoselects me as the 
user. Reminder that you have to enter the Auth code from the url into the prompt on the CL.

Also, add sorting to the status page.
'''


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/api/signed-in-user-details")
async def get_signed_in_user_details():
    try:
        user_details = signed_in_user(None)
        response = {
            "email" : user_details["mail"],
            "first_name" : user_details["givenName"],
            "last_name" : user_details["surname"]
        }
        logger.info(response)
        return response
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/statistics")
async def get_statistics():
    # Replace with real data
    stats = {
        "total_emails_sent": 123,
        "response_rate": 78.5,
        "pending_responses": 26,
    }
    return stats



@app.post("/api/send-emails")
async def send_emails(file: UploadFile):
    try:
        logger.info(f"Received file: {file.filename} with content type: {file.content_type}")

        if os.path.exists("sent_df.csv"):
            logger.info("sent_df exists")
            sent_df = pd.read_csv("sent_df.csv")
        else:
            sent_df = pd.DataFrame(columns=["Property_Name", "Email_Address", "status_code", "Sent", "Time_Sent"])

        # Read the file content
        content = await file.read()
        logger.debug("File content read successfully.")

        if file.content_type in ["application/vnd.ms-excel",
                                 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
            df = pd.read_excel(io.BytesIO(content))
        elif file.content_type == "text/csv":
            df = pd.read_csv(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type.")

        logger.info(f"Dataframe created with shape: {df.shape}")

        email_columns = ["Email", "Email2", "Email3", "Email4"]  # List of possible email columns
        for _, row in df.iterrows():
            property_address = row["Property Address"]
            property_name = row["Property Name"]

            for email_col in email_columns:
                email_address = row.get(email_col, None)
                name_col = email_col.replace("Email", "Name")  # Match email column with the corresponding name column
                name = row.get(name_col, "")

                if pd.isna(email_address) or not email_address:
                    continue  # Skip if email is blank or NaN

                subject = f"Reaching out about {property_name}"

                body = email_template(name, property_name)

                response = send_email(subject, body, email_address)

                if response:
                    sent = response.status_code == 202
                    new_row = pd.DataFrame({
                        "Property_Name": [property_name],
                        "Email_Address": [email_address],
                        "status_code": [response.status_code],
                        "Sent": [sent],
                        "Time_Sent": [datetime.datetime.now() if sent else None]
                    })
                else:
                    new_row = pd.DataFrame({
                        "Property_Name": [property_name],
                        "Email_Address": [email_address],
                        "status_code": [0],
                        "Sent": [False],
                        "Time_Sent": [None]
                    })

                sent_df = pd.concat([sent_df, new_row], ignore_index=True)

        sent_df.to_csv("sent_df.csv", index=False)
        return {"message": "Emails sent successfully", "results": sent_df.to_dict('records')}

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/email-responses")
async def get_email_responses():
    logger.debug("Successful call")
    try:
        if os.path.exists("sent_df.csv"):
            logger.info("sent_df exists")
            sent_df = pd.read_csv("sent_df.csv")
            email_responses = []

            for _, row in sent_df.iterrows():
                try:
                    # Construct search query
                    search_query = f"from:{row['Email_Address']}"

                    # Get email responses
                    response = search_emails(access_token=None, search_query=search_query)

                    # Prepare the email response dictionary
                    email_response = {
                        "property_name": row["Property_Name"],
                        "email": row["Email_Address"],
                        "responded": bool(response),
                        "emails": len(response),
                    }

                    logger.info(email_response)
                    #
                    # Append the dictionary to the list
                    email_responses.append(email_response)
                except Exception as row_error:
                    logger.error(f"Error processing row {row['Property_Name']}: {row_error}")
            return email_responses

        else:
            logger.warning("sent_df.csv does not exist")
            return {
                "error": "sent_df.csv does not exist",
                "email_responses": []
            }
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")



def validate_file_type(file: UploadFile):
    # Get file extension
    filename = file.filename
    extension = Path(filename).suffix.lower()

    # List of allowed extensions and MIME types
    allowed_extensions = {'.xlsx', '.xls', '.csv'}
    allowed_mimes = {
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # xlsx
        'application/vnd.ms-excel',  # xls
        'text/csv',  # csv
        'application/csv'  # csv (alternative)
    }

    # Check extension
    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )

    # Check MIME type
    content_type = file.content_type
    if content_type not in allowed_mimes:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {content_type}"
        )

    return True


# Run the app using: uvicorn main:app --reload --log-level debug
