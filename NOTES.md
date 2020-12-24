Imagine you are a member of a test organization. Implement a program that will retrieve information from the hubstaff V1 API about the time that each employee of the organization spent working on each project. Present the aggregated information in an HTML table.

In the columns, there should be the employees, in the rows, there should be the projects, and in the cells in the middle, there should be the amount of time that a given employee spent working on a given project. The program should only present the projects that were worked on, and the employees who worked on a given day. 

The table should always be rendered for one day, which by default is yesterday. The output should be saved to a file. The configuration (such as the API key) should be read from a config file. A future extension may be for the program to send the table to a manager via email.

It should be possible for a sysadmin to ddoeploy the program on a server without reading its code or running any API queries manually.

There are no hidden requirements. As we have already mentioned, if something was not specified, it means that we expect you to make a choice yourself using your best judgment. For example, we’re not telling you what external libraries or standard library classes you should or should not use.


TO-D0s
1. Hubstaff API V1 to be used
2. Explore V1 APIS and list down necessary ones
3. List necessary parameters and APIs


Notes:
* System interacts or fetches data from hubstaff site about particular organization so that one can track time record of projects and its assiginee and displays in an HTML table

* Tabular presentation of projects, employee and time spent by any employee on any project
Rows -> Project
Column -> Employee
Cell -> Time spent by any employee on that project

* Data that is to be gathered is of yesterday. 

* Output file must be saved. (HTML)

* Use env files for API configuration

* May have future extension for sending email to manager via email.

* Must be deploy ready without any hassle(Use docker. create docker file)

URLS have ratelimiter cannot request authentication token each time. Must save in env.
APIs Needed
1. Authentication (/auth, POST)
    Obtain auth token for a user

    Params:
        email: Have
        password: Have
        app_token: Create app from dev portal to get
    
    Returns:
        auth_token

2. Activities (/activities, GET)
    Retrieve activities

    Params:
        auth_token:
        app_token:
        start_time:
        stop_time:
        organizations:
        projects:
        users:

3. Projects (/organizations/{id}/projects, GET)
    Retrieve projects

    Params:
        auth_token:
        app_token:
        org_id:
        status: active/archived

4. Organizations (/organizations, GET)
    Retrieve organizations

    Params:
        auth_token:
        app_token:

5. Users (/organizations/{id}/members, GET)
    Retrieve users

    Params:
        auth_token:
        app_token:
        org_id:
        organization_memberships: Bool
        project_memberships: Bool