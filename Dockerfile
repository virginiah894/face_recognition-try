# set the base image from host os
FROM  python:3.8.3

# set the working directory in the container
WORKDIR /app

# copy of dependancies to the working directory
COPY requirements.txt .

#  Installing dependancies
RUN pip install -r requirements.txt
# Copy the content of local src directory to the working directory
COPY src/ .
# command to run for starting the container/executables
CMD ['python','run face-rec.py']