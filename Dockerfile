FROM ubuntu:latest

# ----- CODE BOT SETUP ------

# Install all the libs we're going to need.
RUN apt-get update && apt-get install -y python3 python3-pip cron vim

#we are adding our core files.
COPY settings.json challenge.txt main.py emailWorker.py ./

RUN python3 -m pip install -U discord.py

# ----- CRON JOB SETUP ------

# Copy email-cron file to the cron.d directory
ADD crontab /etc/cron.d/email-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/email-cron

# Apply cron job
RUN crontab /etc/cron.d/email-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the commands on container startup
CMD cron && python3 main.py
