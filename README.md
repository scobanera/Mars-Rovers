# Mars-Rovers

> _A squad of robotic rovers are to be landed by NASA on a plateau on Mars. This plateau, which is curiously
rectangular, must be navigated by the rovers so that their on-board cameras can get a complete view of the
surrounding terrain to send back to Earth. [...]_

THe proposed solution is organized in two independent services:
1. *Navigation service*: REST API that controls rovers navigation on the grid. It contains the logic to avoid sending rovers outside of the plateau.
2. *User interface*: provides a (very) simple UI to visualize the plateau grid, rovers landing, and their final position after executing certain commands.

Before describing the solution more in depth, a few key assumptions:
* Rovers will execute commands while within the grid. Any command that would place the rover outside the grid will be ignored.
* Multiple rovers can be placed on the same grid cell.

# Design Overview 

Each service is completely independent and it's hosted in Google Cloud (App Engine). As it can be seen below, the Navigation API and the User Interface are two services under the same Google Cloud project:
![Services](https://user-images.githubusercontent.com/75647943/105783337-fc512500-5f54-11eb-8923-08bb172da19e.PNG)


## Navigation API 
The backend provides the following endpoints:
- /rovers/list
- /rovers/create
- /rovers/\<id\>/move
- /rovers/delete
- /grid/size
- /grid/resize
  
The API can be accessed here: https://navigation-dot-scobanera-mars-rover-ibm.rj.r.appspot.com/. The home path is just reserved to show the API is active.

For example, a GET request to https://navigation-dot-scobanera-mars-rover-ibm.rj.r.appspot.com/grid/size will return the current grid size.

## Storage

Once rovers are palced on the plateau, they will be probably remain on the planet for a few years as most NASA missions. It's important to store the Rovers information beyond a single session, and that's why a database is used. 
_Note: just for simulation purposes, after refreshing the website the old rovers are not present in the plateau. Additionally, after resizing the gird it's assumed that rovers are taken out from the plateau. Changing these behaviors would not impact the overall design_

A MySQL database is used, hosted on Google Cloud SQL:

![databases](https://user-images.githubusercontent.com/75647943/105783324-f9eecb00-5f54-11eb-8d6b-54819401713e.PNG)

The schema for the two tables can be found here:
![databases2](https://user-images.githubusercontent.com/75647943/105783328-fa876180-5f54-11eb-864a-04e070afbabd.PNG)

## User Interface

The user interface is created using HTML, CSS and JavaScript. It makes use of the Navigation API to create, delete, and move rovers.

It can be accessed here: https://user-interface-dot-scobanera-mars-rover-ibm.rj.r.appspot.com/

# Deployment

A minimal flask service is provided to test the User Interface on localhost. It can be tested running `python app.py` on the Frontend folder.

Both backend and frontend directories contain an app.yaml file with the neccesary configurations. Deployment is completed using the Google Cloud SDK.

```
gcloud app deploy
```
Note that backend can also be run on localhost, but it will attempt to connect to the production database. This requires some additional setup that it's detailed here: https://cloud.google.com/sql/docs/mysql/connect-overview

# Example

The instructions document proposes the following input:
```
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
```

That is expected to return the following output:
```
1 3 N
5 1 E
```

In order to replicate this input using the UI developed, we can start by selecting a 6 x 6 grid (the top right coordinate is specified (5,5), creating a grid that goes from (0,0) to (5,5), i.e: 6 rows and 6 columns).
![Home](https://user-images.githubusercontent.com/75647943/105783330-fb1ff800-5f54-11eb-8f22-00fc5e7c0eea.PNG)

Under the `Send Rover` section, we can create the two rovers: `1 2 N` and `3 3 E`
![Home_placed](https://user-images.githubusercontent.com/75647943/105783333-fbb88e80-5f54-11eb-907e-ba413214c807.PNG)

Finally, their respective commands are sent: `LMLMLMLMM` and `MMRMMRMRRM` and we can see that the End Position for each rover matches the expected output:
![Home_final](https://user-images.githubusercontent.com/75647943/105783331-fb1ff800-5f54-11eb-9f94-8131ca53a5b5.PNG)

Further commands can be sent, and rovers will be repositioned accordingly on the grid. As two possible edges cases we can see that:

1. If another rover is placed on the same location, the two of them will share the grid:
![Home_placed_2](https://user-images.githubusercontent.com/75647943/105783334-fbb88e80-5f54-11eb-94cc-23b5d12a7d4b.PNG)

2. If an invalid command is sent (for example, trying to send the rover outside of the plateau), the same will be executed until its last valid position, and all the remaining commands will be ignored.
![Home_placed_3](https://user-images.githubusercontent.com/75647943/105783336-fc512500-5f54-11eb-9a98-8970db265bd0.PNG)

# TODO

There are a few pending tasks to improve the overall project quality:
 - Unit tests.
 - Improve frontend architecture. Although it's a simple UI for demostration purposes, adding new functionalities with the existing approach could lead to certain issues.
 - Improve error handling and error propagation.
 - The API does not use any authentication method at the moment.
 - Using an ORM could simplify the object mapping and database manipulation in general.


