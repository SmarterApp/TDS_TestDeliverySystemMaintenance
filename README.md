# Welcome to the TDSmaintenanceDev Project

The TDSmaintenance Project is a JAR which performs maintenance/cleanup on the TDS (Test Delivery) database. It should be set up to run as a daily cron job. It looks for testopportunities that are not marked completed, their status is not in ("completed", "submitted", "scored", "expired", "reported", 'invalidated'), and their expire timestamp is older than the configured number of hours. If it finds any, it cleans them up.

## License ##
This project is licensed under the [AIR Open Source License v1.0](http://www.smarterapp.org/documents/American_Institutes_for_Research_Open_Source_Software_License.pdf).

## Getting Involved ##
We would be happy to receive feedback on its capabilities, problems, or future enhancements:

* For general questions or discussions, please use the [Forum](http://forum.opentestsystem.org/viewforum.php?f=9).
* Use the **Issues** link to file bugs or enhancement requests.
* Feel free to **Fork** this project and develop your changes!

## Module Overview

### Java

Essentially, this is a Java module with a Java class, with a main method having implementation for maintenance of testopportunities.

For each applicable test opportunity record inserted into archive database opportunityaudit table, If applicable test opportunity had any activity associated with it, test opportunity record itself is updated with status "completed" and date completed is set to the date of the last activity. Otherwise, applicable test opportunity is marked "expired" and dateExpired is set to current timestamp.

In both cases TDSReport is produced for each applicable test opportunity. TDSReports are placed into directory defined by configuration variable TDSReportsRootDirectory. 

## Setup
In general, build the code and deploy the JAR file. A cron job must be set up for running TDSMaintenance.
An example cron job is shown below. Create a bash script with the following data and configure the cron job to run daily at a particular time. crontab settings to run job everyday at 2:00am:
`00 2 * * * user /bin/bash /path/to/base/script`

```
/usr/bin/java \
    -Dlogfilename="/path/to/log/file/maintenance" \
    -Djdbc.driver="com.mysql.jdbc.Driver" \
    -Djdbc.url="jdbc:mysql://name.of.mysql.server:3306/session" \
    -Djdbc.userName="<mysql_username>" \
    -Djdbc.password="<mysql_password>" \
    -DDBDialect="MYSQL" \
    -classpath ".:/jar/file/path/to/tdsMaintenance.jar:/mysql/connector/path/mysql-connector-java-5.1.22-bin.jar" org.opentestsystem.tds.maintenance.Maintenance

```

### Build Order

If building all components from scratch the following build order is needed:

* shared-db
* shared-tr-api
* tdsdlldev

## Dependencies
TDSmaintenanceDev has a number of direct dependencies that are necessary for it to function.  These dependencies are already built into the Maven POM files.

### Compile Time Dependencies
* shared-db
* shared-tr-api
* tds-dll-api
* tds-dll-mysql
* c3p0
* mysql-connector-java
* log4j
* slf4j-log4j12