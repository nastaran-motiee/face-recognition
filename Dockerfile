# For more information, please refer to https://aka.ms/vscode-docker-python
FROM continuumio/miniconda3


# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

WORKDIR /app
COPY . /app

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "smart-elevator-env", "/bin/bash", "-c"]

COPY run.py .
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "smart-elevator-env", "python", "run.py"]
