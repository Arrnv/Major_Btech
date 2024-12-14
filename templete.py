import os
from pathlib import Path
import logging


logging.basicConfig(level=logging.INFO)

listOfFile = [
    
    ".github/workflows/.gitkeep",
    f"src/__init__.py",
    f"src/components/__init__.py",
    f"src/components/dataInject.py",
    f"src/components/dataTransformation.py",
    f"src/components/modeltrainer.py",
    f"src/components/modelmoniter.py",
    f"src/pipeline/__init__.py",
    f"src/pipeline/training_pipeline.py",
    f"src/pipeline/prediction_pipeline.py",
    f"src/exception.py",
    f"src/logger.py",
    f"src/utils.py",
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