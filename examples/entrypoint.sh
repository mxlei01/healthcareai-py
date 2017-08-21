# Start the SQL Server
/opt/mssql/bin/sqlservr --accept-eula &

# Wait for the Microsoft SQL server to be ready
sleep 120s

# Run the setup script to create the DB and the schema in the DB
# -S [protocol:]server[\instance_name][,port]
#       Specifies the instance of SQL Server to which to connect. It sets the sqlcmd scripting variable SQLCMDSERVER.
# -U login_id
#       Is the login name or contained database user name. For contained database users you must provide the database
#       name option (-d).
# -P password
#       Is a user-specified password. Passwords are case sensitive. If the -U option is used and the -P option is not
#       used, and the SQLCMDPASSWORD environment variable has not been set, sqlcmd prompts the user for a password. To
#       specify a null password (not recommended) use -P "".
# -d db_name
#       Issues a USE db_name statement when you start sqlcmd. This option sets the sqlcmd scripting variable
#       SQLCMDDBNAME. This specifies the initial database. The default is your login's default-database property. If the
#       database does not exist, an error message is generated and sqlcmd exits.
# -i input_file[,input_file2...]
#       Identifies the file that contains a batch of SQL statements or stored procedures. Multiple files may be
#       specified that will be read and processed in order. Do not use any spaces between file names. sqlcmd will first
#       check to see whether all the specified files exist. If one or more files do not exist, sqlcmd will exit.
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P yourStrongPassword1234 -i setup.sql

sleep infinity