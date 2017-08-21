# Microsoft has released a Microsoft SQL server for Linux in Docker Hub
FROM microsoft/mssql-server-linux:latest

# Copy our entrypoint and setup.sql files into docker
COPY entrypoint.sh entrypoint.sh
COPY setup.sql setup.sql

CMD /bin/bash ./entrypoint.sh