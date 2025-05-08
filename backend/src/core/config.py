from dotenv import load_dotenv
import os
from sqlmodel import create_engine

load_dotenv()

# gemini
GENAI_KEY = os.getenv("GENAI_KEY")


# log dir
LOG_DIR = "./logs"

# file dir
INPUT_DIR = "/home/khaliq/Documents/Upworks/ProofReader/inputs"
OUTPUT_DIR = "/home/khaliq/Documents/Upworks/ProofReader/outputs"

# Database
SQLITE_URL = "sqlite:///status.db"

connect_args = {"check_same_thread": False}
engine = create_engine(SQLITE_URL, connect_args=connect_args)
