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
* retrieve data with GET /api/members
* <b>returns:</b> a template with user name, role they're seeking, links to their github & linkedIn, as well as project cards for those they contributed to. Project cards include the role they held during that sprint.
* route file path/name: routes/landing.py
* template file path/name: templates/profile.html

## <b>GET</b> /members
### user navigates to Members page from either About Us or Projects
* retrieve data with GET /api/members
* <b>returns:</b> a template with a list of member cards displaying their name, role they are seeking, and a prompt to view their profile ('see more' or something to that effect)
* route file path/name: routes/landing.py
* template file path/name: templates/members.html
---

## API ENDPOINTS

## <b>GET</b> api/members
### used to retrieve a jsonified representation of all members
- gets all members from the firebaseClient using .get_all_by_class('members')
- <b>returns:</b>
    If members are found:
        * jsonified dictionary with:
            * 'status': 'OK'
            * 'members': list of dictionary representations of all members
        * status code of 200
    Otherwise:
        * jsonified dictionary with:
            * 'status': 'error'
            * 'members': empty list
        * status code of 400
- route file path/name: api/v1/members.py

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
- route file path/name: api/v1/projects.py

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
- route file path/name: api/v1/projects.py

---

## MODELS

### FirestoreClient
Handle connections to the firestore database
* ### <b>attributes</b>
    * db - firestore connection (instance)
* ### <b>methods</b>
    * get_all_by_class - retrieve all objects of a given class name (instance)
        * <b>parameters:</b> 
            1. class_name - name of the class to retrieve
        * <b>returns:</b> a <u>list of dictionary representations</u> of all objects of class class_name
    * connected - <b>returns</b> true if database connection is working, else false
- route file path/name: models/firestore_client.py


---
### Project
Information related to each HMC project
* ### <b>attributes</b>
    * name: string - title of the project
    * description: string - description of the project
    * contributors: list of strings for each member id
    * link: string - url to project page, if one exists
    * tech: string of tech ids
- route file path/name: models/projects.py

---
### Tech
Tech stack object
* ### <b>attributes</b>
    * name: string - name of the tech, ex: 'Flask'
    * class: string - css classname for icon
    * projects: list of strings of project ids
    * members: list of strings of member ids for those who've used that tech
- route file path/name: models/tech.py

---
### Members
Members of HMC
* ### <b>attributes</b>
    * id: string - uuid
    * firstname: string - first name
    * lastname: string - last name
    * bio: string - paragraph written by student
    * github: - string - url
    * linkedin: string - url
    * projects: list of strings of project ids
    * title: string - whatever title they want to give themselves
    * tech: list of strings of tech ids they've worked with before
- route file path/name: models/members.py
