#from cicdservices.src.classes import gitlab, github, vercel, jenkins, dataClass
#import src.classes.gitlab as GitLab
#import src.classes.github as GitHUb
import sys

#from decouple import config

#from src.service.src.classes.dataClass import DataClass
#from src.service.src.classes.github as GitHub
#from src.service.src.classes.gitlab import GitLabAPI
import src.service.src.classes.gitlab as Giltlab
#from src.service.src.classes.jenkinsAPI as Jenkins
#from src.service.src.classes.vercelAPI as VercelApi
#from src.classes.Suppliers import RepoCICD
#from src.classes.dataClass import Repository, TypeProjectTemplate
#from github import Github, GithubException
GROUP = "novateva-operations"
USER_VERCEL = "Projectmanager@novateva.com"
PASSWORD_VERCEL = "I8ggFhjQ1oBD"

TOKEN_GITLAB = "glpat-gNv8TsTWTcKqmgrf_VkY"
LINK_VERCEL = "https://vercel.com/%s"
LINK_NEW_PROJECT = "https://vercel.com/new/%s"
LINK_GIT = "https://%s:%s@gitlab.com/novateva/%s.git"
LINK_CONFIG = "http://45.82.73.205:8090/manage/configure"
LOGIN = False
USER_JENKINS="novateva"
PASSWORD_JENKINS="Novateva*2022"
LINK_JENKINS = "http://jenkins.novateva.tech/"

def CreateRepo():
    try:
        #Provider = GitLab.GitLabAPI("")
        #Provider = GitHUb.GitHubAPI("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")
        #repo = Repository(name="NewVersionPackage", users=['6477028'])
        #repoClone = Data.DataClass(NameProject="testClone", LinkGit=LINK_GIT)
        #print(repoClone.CloneUrl)
        #clone = TypeProjectTemplate(name="testClone", repo_template="44481200", branch="main", provider=TypeProject.Jenkins.value, url=repoClone.CloneUrl)
        #print(clone)
        #API = Repo(repositoryClass=Provider, dataRepo=repo, cloneRepo=clone)

        #*******GITHUB**********Lista
        #API = GitHub.GitHubAPI("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")
        #Project = API.create_repo(repo_name="testApiChange") #API.create_repository(repository_name="PackageNew2Ver", users=["mator0296"])
        #Project = API.update_repo(repo_name="testApiChange", new_name="ApiChange")
        #Project = API.get_project(name="nameRepo")
        #Project = API.delete_repo(name="ApiChange")
        #Project = API.create_commit_and_push("nameRepo","main")
        #print(Project)
        #*******GITHUB**********

        #*******GITLAB**********Lista
        API = Giltlab.GitLabAPI("glpat-U-wCyqfezDsG-y66dJao")
        #Project = API.create_repo(repo_name="TestApigti")
        #Project = API.update_repo(repo_name="50499341", new_name="TEST-API", new_description="TEST-API")
        #Project = API.get_project(id="50499341")
        #Project = API.delete_repo(repo_name="50499341")
        #Project = API.clone_repo(user="ktja", password="kevin2303*", projectId="50500409", branchName="main")
        #Project = API.clone_and_push_repo(f"https://ktja:kevin2303*@gitlab.com/ktja/apiTest.git", "apiTest", "vercel", "True")
        Project = API.create_commit_and_push(name="testnewzip",branch="main", nameZip="CodeGenerator.zip", is_zip=True, type="Back" )
        print(Project)
        #*******GITLAB**********

        #*****JENKINS***********#Lista
        #data = Data.DataClass(User=USER_JENKINS, Password=PASSWORD_JENKINS, NameProject="Payment-module-jenkins", updateProject="code-generator2", Link =LINK_JENKINS, LinkGit=LINK_GIT, GitUser="novateva", GitPassword="I8ggFhjQ1oBD", Token=TOKEN_GITLAB )
        #Provider = Jenkins.JenkinsInterface(data)
        #API = Provider.CreateProject()
        #API = Provider.UpdateProject()
        #API = Provider.DeleteProject()
        #API = Provider.ReadProject()
        #API = Provider.get_link_Create_Project()
        #result = Provider.CreateProject()
        #result = API.delete_cicd_from_repository()
        #result = API.update_cicd_in_repository()
        #print(result)
        #*****JENKINS***********#

        #*****VERCEL API***********#Lista

        #buildCommand,devCommand,repo,type,installCommand,outputDirectory,rootDirectory BuildOptions=["vite build","vite --port $PORT", "testApi", "gitlab", "npm install", "dist"]
        '''data = Data.DataClass(nameProject="testlambdavercel", updateProject="verceltestdesdeapi3", framework="vite", projectID="prj_ME5C57X45zed5VuYAJi2eycseBBm", buildOptions=["vite build","vite --port $PORT", "testApi", "gitlab", "npm install", "dist"],
                              env=[{"key": "VARIABLE_1", "value": "VALOR_1", "target": "production", "type": "plain"}], user="kevin.torres@novateva.com", password="kevin2303*", group="team_HFjyG4RdbIeFralE86LXV4Yp", tokenAPI="tJ5I3H23riqZNf5ZyxReoVYN")'''
        #data = Data.DataClass(nameProject="front-clonezip", updateProject="testlambdaapi2", framework="vite", projectID="prj_L4fNWyHfEBw54YDjDUaiQkLhY9uH", buildOptions=["vite build","vite --port $PORT", "front-clonezip", "gitlab", "npm install", "dist"],
        #                      env=[{"key": "VARIABLE_1", "value": "VALOR_1", "target": "production", "type": "plain"}], user="kevin.torres@novateva.com", password="kevin2303*", group="team_HFjyG4RdbIeFralE86LXV4Yp", tokenAPI="tJ5I3H23riqZNf5ZyxReoVYN")
        #for update BuildOptions=["vite build","vite --port $PORT", "vite", "npm install", "dist"]
        #data = Data.DataClass(nameProject="front-clonezip", updateProject="testlambdaapi2", framework="vite", projectID="prj_0JhkJRzGDMsfkEGj0ltdXs74BkI5", buildOptions=["vite build","vite --port $PORT", "front-clonezip", "gitlab", "npm install", "dist"],
        #                      env=[{"key": "VARIABLE_1", "value": "VALOR_1", "target": "production", "type": "plain"}], user="kevin.torres@novateva.com", password="kevin2303*", group="team_HFjyG4RdbIeFralE86LXV4Yp", tokenAPI="tJ5I3H23riqZNf5ZyxReoVYN")
        #Provider = VercelApi.VercelInterfaceAPI(data)
        #API = RepoCICD(providerClass=Provider)   
        #result = API.add_cicd_to_repository()
        #result = API.read_cicd_from_repository()
        #result = API.update_cicd_in_repository()
        #result = API.update_cicd_in_repository()
    
        #API = Provider.CreateProject()
        #API = Provider.ReadProject()
        #API = Provider.UpdateProject()
        #API = Provider.DeleteProject()
        #print(result)
        #print(result.get('id'))
        #print(result.get('name'))

        #*****VERCEL  API***********#


        #*****VERCEL selenium***********#
        #data = Data.DataClass(NameProject="testvercel", Framework="vite", updateProject="", BuildOptions= ['test', 'test2', 'test3', 'test4'], Env={"brand": "Ford"})
        #Provider = Vercel.VercelInterface(data)
        #API = Provider.CreateProject()
        #API = Provider.DeleteProject()
        #API = Provider.ReadProject()
        #API = Provider.UpdateProject()
        #API = Provider.get_link_login()ya
        #API = Provider.get_link_new_project()
        #API = Provider.get_link_Read_Project()ay
        #API = Provider.get_link_Delete_Project()ay
        #API = Provider.get_link_Update_Project()ay
        #result = API.add_cicd_to_repository()
        #result = API.delete_cicd_from_repository()
        #result = API.update_cicd_in_repository()
        #print(API)
        #*****VERCEL selenium***********#

    except Exception as err:
        raise Exception(f"Unexpected {err}")

if __name__ == "__main__":
    
      #List sys.argv
        #1 - Group ID
        #2 - Name new project
        #3 - Repository name
        #4 - Branch name
        #5 - User
        #6 - Password
    CreateRepo()

