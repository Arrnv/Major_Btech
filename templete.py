import os
from pathlib import Path
import logging


logging.basicConfig(level=logging.INFO)

projectname = "MajorBtech"

listOfFile = [
    
    ".github/workflows/.gitkeep",
    f"src/{projectname}/__init__.py",
    f"src/{projectname}/components/__init__.py",
    f"src/{projectname}/components/dataInject.py",
    f"src/{projectname}/components/dataTransformation.py",
    f"src/{projectname}/components/modeltrainer.py",
    f"src/{projectname}/components/modelmoniter.py",
    f"src/{projectname}/pipeline/__init__.py",
    f"src/{projectname}/pipeline/training_pipeline.py",
    f"src/{projectname}/pipeline/prediction_pipeline.py",
    f"src/{projectname}/exception.py",
    f"src/{projectname}/logger.py",
    f"src/{projectname}/utils.py",
    "app.py",
    "Dockerfile",
]


for filepath in listOfFile:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory:{filedir} for the file {filename}")

    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath,'w') as f:
            pass
            logging.info(f"Creating empty file: {filepath}")


    
    else:
        logging.info(f"{filename} is already exists")