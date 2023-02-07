FROM python:3.9-slim-buster

WORKDIR /app

# Copy the tar.gz file to the Docker image
COPY dist-test/*.tar.gz .

# Install the required dependencies
RUN pip install *.tar.gz

# Remove the tar.gz file to reduce the size of the Docker image
RUN rm *.tar.gz

# Copy the rest of the code
COPY . .

# Define the entrypoint to run the application
ENTRYPOINT ["scrapy", "crawl", "mercadobitcoin-tickers", "-a", "input_msg=TestInputMsg"]
