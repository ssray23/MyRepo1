# ------------------------------------------------------
#  GitHub Remote Repo (default)
# ------------------------------------------------------
# switch to folder where you want your repos to be 
cd /c/suddha/GitRepos

# clone a remote repo (ONLY if starting on a clean new system where MyRepo1 does not exists)
git clone https://github.com/ssray23/MyRepo1.git

# Get inside your repo just created
cd /c/suddha/GitRepos/MyRepo1/

# Initialize a Git repository with the contents of current working directory 
git init 

# check status of contents in the repository
git status

# add FileA in the directory to the repository
git add FileA

# add FileB inside Folder1 to the repository
git add Folder1/FileB

# add entire Folder2 to the repository
git add Folder2/

# add everything untracked and modified to the repository
git add -A 

# add everything added to the repository
git add .

# removed deleted files from the repository (Note the . after -u)
git add -u .  

# check status .. what has been added/changed/deleted in your local git
git status

# commit changes to local git
git commit -m "My commit"

# check git remote (i.e. repo on github)
git remote --verbose

# remove current remote repository (i.e. GitHub or GitLab)
git remote remove origin

# connect local git to remote github repo (you will get fatal error if already linked to remote)
git remote add origin https://github.com/ssray23/MyRepo1.git

# push to remote repo on the web
git push -u origin master

# ------------------------------------------------------
#  GitLab Remote Repo
# ------------------------------------------------------

# remove current remote repository (i.e. GitHub)
git remote remove origin

# connect local git to remote GitLab repo 
git remote add origin <git@gitlab.com:suddharay/MyRepo1.git  <--- somehow does not work SSH method
git remote add origin https://gitlab.com/suddharay/MyRepo1.git  <---  HTTP works!

# check
git remote --verbose

# push entire local repo to remote repo on the web ....
# ensure that master branch in Gitlab is "unprotected" (generally protected by default) .. 
# change in settings in Gitlab
git push -u origin master
# if the above does not work, try push "force"fully
git push origin master --force

# remove SSL Verification -- this will prompt you for username and password (Bitbucket) when you try to push 
git config --global http.sslVerify false
# if the above does not work, try push forcefully
git push origin master --force

# Alternate way to push entire local to remote in one shot
# Initial Push (to an empty repo on remote)
git push --set-upstream https://gitlab.com/suddharay/MyRepo1.git master

#------------------------------------------------------
#  Bitbucket Remote Repo
# ------------------------------------------------------

# remove current remote repository (i.e. GitHub or GitLab)
git remote remove origin

# connect local git to remote BitBucket repo 
git remote set-url origin git://bitbucket.org/ssray23/myrepo1.git
git remote add origin https://bitbucket.org/ssray23/MyRepo1.git   <--- works

# check
git remote --verbose

# remove SSL Verification -- this will prompt you for username and password 
# (Bitbucket) when you try to push 
git config --global http.sslVerify false

# push entire local repo to remote repo on the web
git push origin master --force

# Alternate way to push entire local to remote in one shot
# Initial Push (to an empty repo on remote)
git push --set-upstream https://bitbucket.org/ssray23/MyRepo1.git master

# Reference1: https://www.datacamp.com/community/tutorials/git-push-pull
# Reference2: https://stackoverflow.com/questions/16330404/git-how-to-remove-remote-origin-from-git-repo
# Reference3: 
