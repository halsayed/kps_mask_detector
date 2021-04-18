FROM tensorflow/tensorflow

RUN apt update && apt install -y libglu1-mesa wget
RUN pip install --upgrade pip
RUN pip install opencv-python
COPY models /models

RUN wget https://s3-us-west-2.amazonaws.com/ntnxsherlock-runtimes/python-env.tgz
RUN tar xf /python-env.tgz
RUN pip install -r /python-env/requirements.txt
# In this example we install Kafka client for Python as additional 3rd party software
RUN pip install kafka-python
USER 10001
# Finally run Python function worker which pull and executes functions.
CMD ["/python-env/run.sh"]

