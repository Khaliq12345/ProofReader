import sys

sys.path.append(".")

from fastapi import FastAPI, HTTPException, BackgroundTasks
from src.core import config
from src.services import document_services
from src.services import ai_services
from src.core.logging import logger
from src.models.status_database import create_db_and_tables
from src.models.status_database import Status
from src.services import database_service

from src.utils import create_folders, file_to_zip

from sqlmodel import select
import os
from datetime import datetime
import asyncio


sem = asyncio.Semaphore(5)  # Limit to 5 concurrent tasks

app = FastAPI(
    title="ProofReader",
    on_startup=[create_db_and_tables, create_folders.create_input_output_folder],
)


async def run_task(folder_path: str, folder_name: str, file_names: list[str]):
    # go through each file and process it
    for idx, file_name in enumerate(file_names):
        try:
            # extract table from file and convert to markdown
            logger.info(f"Converting file to markdown - {file_name}")
            table_md = document_services.pdf_file_name_to_md(
                os.path.join(config.INPUT_DIR, file_name)
            )

            # use llm to generate the analysis
            logger.info("Use llm to generate the analysis")
            parsed = await ai_services.analyse_markdown(table_md)
            if not parsed:
                continue

            # save the parsed analysis to a folder
            ai_services.save_to_csv(
                parsed=parsed,
                output_filename=os.path.join(folder_path, f"analysed_{file_name}.csv"),
            )
        except Exception as e:
            # update the task status with the error
            with database_service.get_session() as session:
                stmt = select(Status).where(Status.folder_name == folder_name)
                status = session.exec(stmt).one()
                if status:
                    status.folder_name = folder_name
                    status.status = "failed"
            logger.error(str(e))

    # convert folder to zip
    file_to_zip.zip_folder(folder_path, os.path.join(folder_path, "output.zip"))

    # update status in database
    with database_service.get_session() as session:
        stmt = select(Status).where(Status.folder_name == folder_name)
        status = session.exec(stmt).one()
        if status:
            status.folder_name = folder_name
            status.status = "success"


@app.post("/api/login")
async def login(email: str, password: str):
    # validate credential
    if (email == config.EMAIL) and (password == config.PASSWORD):
        return {"detail": "success"}

    raise HTTPException(status_code=404, detail="Incorrect credentials")


@app.post("/api/analyse-document")
async def analyse_document(
    backgroundtask: BackgroundTasks, file_names: list[str]
) -> dict:
    try:
        # create a unique folder name
        folder_name = f"output_{datetime.now().timestamp()}"
        folder_path = os.path.join(config.OUTPUT_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # update the db with the task
        with database_service.get_session() as session:
            stmt = Status(folder_name=folder_name)
            session.add(stmt)
            session.commit()

        backgroundtask.add_task(run_task, folder_path, folder_name, file_names)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "started", "output_folder": folder_name}  # test the error


@app.get("/api/check-status/{folder}")
def check_status_of_folder(folder: str):
    # check status of the specified task
    with database_service.get_session() as session:
        stmt = select(Status).where(Status.folder_name == folder)
        response = session.exec(stmt).one()
        return {"status": response.status, "folder": response.folder_name}
    return {"status": None, "folder": None}
