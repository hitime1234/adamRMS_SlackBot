import requests
import json
import functools

class projectObject:
    def __init__(self, name, id, ownerid, owner, clients, subprojects):
        self._name = name
        self._id = id
        self._ownerid = ownerid
        self._owner = owner
        self._clients = clients
        self._subprojects = subprojects

    def getName(self):
        return self._name

    def getID(self):
        return self._id

    def getOwnerID(self):
        return self._ownerid

    def getOwner(self):
        return self._owner

    def getClients(self):
        return self._clients

    def getSubprojects(self):
        return self._subprojects

    def update(self, project):
        self._name = project.getName()
        self._id = project.getID()
        self._ownerid = project.getOwnerID()
        self._owner = project.getOwner()
        self._clients = project.getClients()
        self._subprojects = project.getSubprojects()

    
        


    def __str__(self):
        return f"Name: {self._name}, ID: {self._id}, Owner ID: {self._ownerid}, Owner: {self._owner}, Clients: {self._clients}, Subprojects: {self._subprojects}"

    def __repr__(self):
        return f"_{self._name}_Project"

    def __eq__(self, other):
        return (
            self._name == other.getName()
            and self._id == other.getID()
            and self._ownerid == other.getOwnerID()
            and self._owner == other.getOwner()
            and self._clients == other.getClients()
            and self._subprojects == other.getSubprojects()
        )

    def __ne__(self, other):
        return (
            self._name != other.getName()
            or self._id != other.getID()
            or self._ownerid != other.getOwnerID()
            or self._owner != other.getOwner()
            or self._clients != other.getClients()
            or self._subprojects != other.getSubprojects()
        )

    def __hash__(self):
        return hash(
            (
                self._name,
                self._id,
                self._ownerid,
                self._owner,
                self._clients,
                self._subprojects,
            )
        )
    
    



        


class rms:
    def __init__(self, url):
        self.projects = []
        self._url = url
        self._headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            'Cookie': None
        }
        self._username = None
        self._password = None


    @functools.lru_cache()
    def userList(self, usersString):
        userList = {}
        users = json.loads(usersString)
        for user in users:
            userList[user['users_userid']] = user['users_username']
        return userList

    def getUsername(self,id):
        response = requests.get(f'{self._url}/instances/users.php', headers=self._headers)
        if response.status_code == 200:
            users = response.json()['response']['users']
            usersString = json.dumps(users)
            userList = self.userList(usersString)
            try:
                return userList[id]
            except KeyError:
                return None
        else:
            return None

    def getProjects(self):
        new = []
        response = requests.get(f"{self._url}/projects/list.php",headers=self._headers)
        if response.status_code == 200:
            projects = response.json()['response']
            for project in projects:
                name = project['projects_name']
                id = project['projects_id']
                ownerid = project['projects_manager']
                owner = self.getUsername(ownerid)
                clients = project['clients_name']
                subprojects = project['subprojects']
                new.append(projectObject(name, id, ownerid ,owner, clients, subprojects))
            return new
        else:
            return None
            
    def newProject(self, projects):
        projFlag = False
        new = []
        for project in projects:    
            flag = True
            for old in self.projects:
                if project == old:
                    flag = False
            if flag:
                new.append(project)
                projFlag = True
        if projFlag:
            self.projects = projects
            return projFlag, new
        else:
            return projFlag, None
        

    def update(self):
        projects = self.getProjects()
        if projects:
            flag, New = self.newProject(projects)
            return flag, New
        else:
            return None
    
    def authenticate(self, username, password):
        response = requests.post(f"{self._url}/login/login.php", data={"formInput": username, "password": password})
        self._username = username
        self._password = password
        returnJson = (response.headers)
        header = returnJson['set-cookie'].split(";")[0]
        self._headers['Cookie'] = header
        return response.status_code == 200, 

    def run(self):
        hold = self.authenticate(self._username, self._password)
        if hold:
            print("Authenticated")
            print(self.getProjects())
            return self.update()
        else:
            print("Not Authenticated")
            return None

    def __str__(self):
        return f"Projects: {self.projects}"
    



if __name__ == "__main__":
    file = open("hidden.key","r")
    lines = file.readlines()
    file.close()
    url = lines[1].strip()
    userName = lines[3].strip()
    passw = lines[4].strip()

    rms = rms(url)
    hold = rms.authenticate(userName, passw)
    if hold:
        print("Authenticated")
        print(rms.getProjects())
        print(rms.update())
        print(rms.projects)
        print(rms.update())

    else:
        print("Not Authenticated")
 
    
    
    

    

                    
                
                
                    
                    
    

    

