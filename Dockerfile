FROM tiangolo/uwsgi-nginx-flask:python3.6

# If STATIC_INDEX is 1, serve / with /static/index.html directly (or the static URL configured)
ENV STATIC_INDEX 1
# ENV STATIC_INDEX 0

COPY ./app /app
RUN pip install numpy
RUN pip install pandas
RUN pip install  datetime
RUN pip install colorlover
RUN pip install IPython
RUN pip install plotly
RUN pip install cufflinks
RUN pip install xlrd
RUN pip install openpyxl
RUN pip install flask_cors