from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import csv


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    data: list
    filename: str = "backlog.csv"


class Save_to_csv_Tool(BaseTool):
    name: str = "save_to_csv"
    description: str = (
        "Save a list of dictionaries to a CSV file"
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, data,filename) -> str:
        # Implementation goes here
        if not data:
            return "No data to save."
        keys = data[0].keys()
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        return f"CSV saved as {filename}"
