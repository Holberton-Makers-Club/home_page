# HOLBERTON MAKERS CLUB

### Home page documentation includes:

* stories
* routes
* api endpoints
* models

---
---

## Home page - stories

* ### <b>As a</b> hiring manager
* ### <b>I want to</b> discover compelling student projects
* ### <b>so I can</b> hire skilled junior engineers.
---
* ### <b>As a</b> user
* ### <b>I want to</b> find projects by name
* ### <b>so I can</b> learn more about it.
---


## Home page - routes

## <b>GET</b> /
### user visits the landing page
* <b>returns:</b> a template that showcases projects

## <b>POST</b> /search
### search form on the landing page is submitted
* retrieve data with GET /api/projects/name/\<str: name>
* <b>returns:</b> redirect to landing page with jinja data for projects found

---

## Home page - API

## <b>GET</b> api/projects
### used to retrieve a jsonified representation of all projects
- gets all projects from the firebaseClient
- <b>returns:</b>
    If projects are found:
        * jsonified dictionary with:
            * 'status': 'OK'
            * 'projects': list of dictionary representations of all projects
        * status code of 200
    Otherwise:
        * jsonified dictionary with:
            * 'status': 'error'
            * 'project': empty list
        * status code of 400

## <b>GET</b> api/projects/name/<str: name>
### used to find a project with a given name
- retrieve all projects from <b>GET /api/projects</b>
- checks for a project with the correct name
- <b>returns:</b>
    * If a matching project is found:
        * jsonified dictionary with:
            * 'status': 'OK'
            * 'project': dictionary representation of the project
        * status code of 200
    * Otherwise:
        * jsonified dictionary with:
            * 'status': 'error'
            * 'project': empty dictionary
        * status code of 400

---

## Home page - models

### FirestoreClient
Handle connections to the firestore database
* ### <b>attributes</b>
    * db - firestore connection
* ### <b>methods</b>
    * get_all_by_class - retrieve all objects of a given class name
        * <b>parameters:</b> 
            1. class_name - name of the class to retrieve
        * <b>returns:</b> a <u>list of dictionary representations</u> of all objects of class class_name


---
### Project
Information related to each HMC project
* ### <b>attributes</b>
    * name: string - title of the project
    * description: string - description of the project
    * members: list[strings] - list of team member full names/contributors
    * link: string - url to project page, if one exists