import pandas as pd
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

# Load environment variables from .env file
load_dotenv()

# Load the Excel file into a pandas DataFrame
file_url = os.path.join(os.getcwd(), "usekase.xlsx")
df = pd.read_excel(file_url)

# Connect to MongoDB
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")

# Initialize MongoDB client
client = AsyncIOMotorClient(MONGODB_URI)
db = client[MONGODB_DB_NAME]  # Access the specific database
collection = db["usekase"]  # Replace with your collection name

# Convert the DataFrame to a list of dictionaries
data = df.to_dict(orient="records")


# Insert data into MongoDB asynchronously
async def insert_data():
    await collection.insert_many(data)  # Insert the data asynchronously

    # Verify insertion by printing a few documents asynchronously
    async for document in collection.find().limit(5):  # Adjust the limit as needed
        print(document)


# Run the asynchronous function
asyncio.run(insert_data())
