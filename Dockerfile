FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

# Install cron
RUN apt-get update && apt-get install -y cron

# Add crontab file
ADD src/crontab /etc/cron.d/my-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/my-cron

# Apply cron job
RUN crontab /etc/cron.d/my-cron

# Create the log file to allow running tail
RUN touch /var/log/cron.log

CMD ["cron", "-f"]
