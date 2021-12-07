FROM python:3.9
ENV APP /app
RUN mkdir $APP
WORKDIR $APP
EXPOSE 5000
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
#RUN pip install -r requirements.txt
#RUN mkdir -p /home/pythoh_flask \
#    && mv * /home/pythoh_flask \
#    && cd /home/pythoh_flask \
#    && export FLASK_APP=app \
#CMD flask run