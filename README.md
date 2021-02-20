# HOLBERTON MAKERS CLUB

---
---

## Home page - stories

* ### <b>As an</b> employer
* ### <b>I want to</b> discover compelling student projects
* ### <b>so I can</b> hire skilled junior engineers.
---
* ### <b>As an</b> employer
* ### <b>I want to</b> find projects by name, member name, and tech stack
* ### <b>so I can</b> discover talent that meets my specific needs.
---
* ### <b>As an</b> employer
* ### <b>I want to</b> view specific information about individual project participants
* ### <b>so I can</b> understand their skillset/activity and connect with them.
---
* ### <b>As a</b> student
* ### <b>I want to</b> find detailed information about the value Makers Club provides to students
* ### <b>so I can</b> decide if I would like to get involved.
---
* ### <b>As a</b> potential partner of HMC
* ### <b>I want to</b> understand the mission and activities of HMC
* ### <b>so I can</b> decide if and how we may develop a partnership.
---

## ROUTES

## <b>GET</b> /
### user visits the landing page, which also serves as the About Us page
* <b>returns:</b> a template that displays the what, why, and how to get involved/contact HMC

## <b>GET</b> /projects
### user navigates to the Projects page from either About Us or Meet the Team
* <b>returns:</b> a template that showcases projects and links to member profile pages

## <b>POST</b> /projects/search
### search form on the landing page is submitted
* check the filter input to see if user wants to filter by member name, tech stack, etc.
* retrieve data with GET /api/projects/name/\<str: name>
* if filter is present, apply it to data recieved
* search for matches in appropriate fields, all if no filter is provided
* <b>returns:</b> redirect to landing page with jinja data for projects found

## <b>GET</b> /members/\<id>
### user navigates to an individual member profile page
* retrieve data with GET /api/members/<id>
* <b>returns:</b> a template with user name, role they're seeking, links to their github & linkedIn, as well as project cards for those they contributed to. Project cards include the role they held during that sprint.

## <b>GET</b> /members
### user navigates to Members page from either About Us or Projects
* retrieve data with GET /api/members
* <b>returns:</b> a template with a list of member cards displaying their name, role they are seeking, and a prompt to view their profile ('see more' or something to that effect)

---

## API ENDPOINTS

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

## MODELS

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
