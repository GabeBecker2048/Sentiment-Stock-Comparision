FROM almalinux:9

RUN dnf install -y epel-release
RUN dnf config-manager --set-enabled crb
RUN dnf install -y python-pip python3-pip R && dnf clean all

# COPY and CMD instructions for your Python and R program
# For example:
COPY . /app
WORKDIR /app
RUN pip3 install --no-cache-dir -r requirements.txt

RUN Rscript -e "install.packages(c('dplyr', 'tidytext', 'ggplot2', 'tidyr'), repos='https://cloud.r-project.org')"
#CMD python -u main.py -run  # adjust as needed

# docker run -v ./lib:/app/lib sentiment-stock-image
