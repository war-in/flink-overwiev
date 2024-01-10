# Use an official OpenJDK image as a parent image
FROM openjdk:11

# Set the JAVA_HOME environment variable
ENV JAVA_HOME /usr/local/openjdk-11

# Add JAVA_HOME/bin to the PATH environment variable
ENV PATH $JAVA_HOME/bin:$PATH

# Install Python and other dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Set the Python executable in the PATH
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# Verify installations
RUN java -version && \
    python --version && \
    pip3 --version

# Set the working directory to /app
WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install poetry
RUN poetry install

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt

# Run script.py when the container launches
#CMD ["poetry", "run", "python", "main.py"]
CMD ["poetry", "run", "python", "flink_overview.py"]