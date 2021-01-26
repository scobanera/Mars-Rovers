# Mars-Rovers

> _A squad of robotic rovers are to be landed by NASA on a plateau on Mars. This plateau, which is curiously
rectangular, must be navigated by the rovers so that their on-board cameras can get a complete view of the
surrounding terrain to send back to Earth. [...]_

This solution to the problem is organized using two main services:
1. *Rest API*: it controls the rovers and how they can move over the grid
2. *User interface*: provides a (very) simple UI to visualize the plateau grid, rovers landing, and their final position after executing certain commands.

Before describing the solution more in depth, a few key assumptions:
* Rovers will execute commands while within the grid. Any command that would place the rover outside the grid will be ignored.
* Multiple rovers can be placed on the same grid cell.

# Design Overview 

Each service is completely independent and it's hosted in Google Cloud (App Engine).

The backend provides the following endpoints:
- /rovers/list
- /rovers/create
- /rovers/<id>/move
- /rovers/delete
- /grid/size
- /grid/resize
  
The backend can be accessed here: https://navigation-dot-scobanera-mars-rover-ibm.rj.r.appspot.com/. The home path is just reserved to show the API is active.

For example, a GET request to https://navigation-dot-scobanera-mars-rover-ibm.rj.r.appspot.com/grid/size will return the current plateau size.

# User Interface

The user interface is created using HTML, CSS and JavaScript, It makes use of the API to create, delete, and move rovers.

It can be accessed here: https://user-interface-dot-scobanera-mars-rover-ibm.rj.r.appspot.com/

# Deployment

A minimal flask service is provided to test the User Interface on localhost. It can be tested running `python app.py`

Both backend and frontend directories contain an app.yaml file with the neccesary configurations. Deployment can be achieved by running:

```
gcloud app deploy
```
Note that backend can also be run on localhost, but it will attempt to connect to the production database. This requires come additional setup that it's specified here: https://cloud.google.com/sql/docs/mysql/connect-overview

# Notes

There are a few pending tasks to improve the project:
 - Using an ORM could simplify the object mapping and database manipulation in general.
 - Unit tests are pending.
 - The frontend does not particulatly follow UI/UX best practices and it's for demonstration purposes.
 - The API does not use any authentication method at the moment.
