from google import genai
from google.genai import types
from src.constants import document_system_prompt
from src.core import config
from src.models import analysis
from typing import Optional
from the_retry import retry
import json
import pandas as pd
import os

client = genai.Client(api_key=config.GENAI_KEY)


@retry(attempts=5)
async def analyse_markdown(table_markdown: str) -> Optional[analysis.Analysis]:
    # use genai to get an analysed structured output
    response = await client.aio.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Analyse this mardown table: {table_markdown}",
        config=types.GenerateContentConfig(
            system_instruction=document_system_prompt.system_prompt,
            response_mime_type="application/json",
            response_schema=analysis.Analysis,
        ),
    )

    if response.parsed:
        return response.parsed
    return None


def save_to_csv(parsed: analysis.Analysis, output_filename: str) -> None:
    # load the response from gemini and save to a file
    results = json.loads(parsed.model_dump_json())
    df = pd.DataFrame(results["results"])
    df.to_csv(os.path.join(config.OUTPUT_DIR, output_filename))

    return None
