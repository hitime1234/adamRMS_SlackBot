from adamrms import rms;
from SlackHandler import slackAPI;

file = open("hidden.key","r")
lines = file.readlines()
file.close()
token = lines[0].strip()
url = lines[1].strip()
channel = lines[2].strip()
user = lines[3].strip()
passw = lines[4].strip()



class main:
    def __init__(self,token,url,channel,user,passw):
        self.url = url
        self.rms = rms(url)
        self.slack = slackAPI(token)
        self.slack.setChannel(channel)
        hold = self.rms.authenticate(user,passw)
        if hold == False:
            print("Authentication failed")
            return
        else:
            print("Authenticated")
        
    
    def run(self):
        self.slack.sendMessage("Eng BOT is here!")
        Check, projects =  self.rms.run()
        if Check:
            for project in projects:
                self.slack.sendMessage(f"*#Check with eng:*\nProject Name: {project.getName()}\nOwner: {project.getOwner()}\nClient: {project.getClients()}\nSubProjects: {project.getSubprojects()}\nLink: https://dash.adam-rms.com/project/?id={project.getID()}\n")



        

    

if __name__ == "__main__":
    main = main(token,url,channel,user,passw)
    main.run()