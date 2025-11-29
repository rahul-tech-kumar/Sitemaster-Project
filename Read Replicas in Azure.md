#         **Read Replicas in Azure Database for MySQL**







         - MySQL is one of the most popular database engines for running internet-scale web and mobile applications.

         - We will work on the MYSQL Flexible Server.

         - It(Flexible Server) is widely used across domains such as online education, digital payments, e-commerce, gaming, healthcare,  and more.

 

 



         - WE migrate the  applications scale using services like Azure Virtual Machine Scale Sets, Azure App Services, or Azure Kubernetes Service (AKS), the database often becomes a performance bottleneck because it is a stateful centralized component.





         - This replication uses MySQL’s built-in binlog replication, which tracks changes and replays them on replicas.

         - Whenever data is written to the main MySQL server, the changes are recorded in a binary log (binlog).

 



##               **Replica Management \& Billing**



        - Billing is based on compute and storage per month.

        - Read replicas are only supported in **General Purpose** or **Business Critical pricing tiers**.





##               **Use Cases for Read Replicas**

        -  BI and analytical workloads

        -  Uses asynchronous replication → replicas eventually consistent









 

##                   **Create a replica**

        - When you start the create replica workflow, you create a blank Azure Database for MySQL Flexible Server instance.



        - The creation time depends on the amount of data on the source and the time since the last weekly full backup.

 

        - After signup selecting the existing Azure DataBase for MySQL Flexible Server instances.

        - Go to the setting and choose Replication



        - There is a option in left up side ADD replica



        - Enter the name for replica server



        - Choosing the Availability Zones



        - Enter location based on your need to create an in-region



        - Selecting the Faster Provisioning (Temporarily boosting IOPS helps accelerate the replica provisioning process)



        -  Its created then you can see on Replication page.







##                **Stop Replication**

         - We will select the option **PROMOTE** that is visible on the replication Page to stop the replica server.

 





##                **Delete Replica Server**

         - After stoping ,You will see their is a option just beside the Promote ...DELETE





##                Delete Replica source Server

         - In the Azure portal, select your source Azure Database for MySQL Flexible Server instance.



         - From the Overview, select Delete.



##                Monitor replication

         - In the Azure portal, select the replica Azure Database for MySQL Flexible Server instance you want to monitor.



         - Under the Monitoring section of the sidebar, select Metrics:



         - Select Replication lag in seconds from the dropdown list of available metrics.



         - Select the time range you wish to view. The image below selects a 30-minute time range.









\#-----------------------------------------------------------------------------------------------------------------------------------------

## &nbsp;              Virtual Machine

&nbsp;        - HOME --> Computer Infrastructure --> Virtual Machines

&nbsp;        - In overview there is a option to start the virtual machine.

&nbsp;        - Go to the connect Version and then download a RDP TO connect the server.

&nbsp;        - Then go into the your own system search bar to search RDC(Remote Desktop Connection).
         - After putting the IP Address and port No.
         - ITS connected now we can run .





