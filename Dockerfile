# Use an official Python runtime as a base image
#python:2.7-slim
FROM scratch
FROM dockercisco/acitoolkit:latest

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app
COPY * /app/

# Install any needed packages specified in requirements.txt

RUN apt-get -yqq update
#RUN apt-get install -yqq python
RUN apt-get -yqq install python-pip
RUN apt-get install net-tools
#RUN apt-get install iptables
RUN apt-get -yqq install vim
RUN pip install ciscosparkapi
RUn pip install Flask
RUN pip install -r requirements.txt
#RUN rm /bin/sh && ln -s /bin/bash /bin/sh
#RUN /bin/bash -c "source /app/token.sh"

#RUN . token.sh


#CMD ["source /app/token.sh"]

#CMD ["/bin/bash"]
#CMD ["/app/start.sh"]
#CMD ["python", "app.py"]
