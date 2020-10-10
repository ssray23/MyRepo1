# Get inside your repo just created
cd /c/suddha/GitRepos/MyRepo1/

# Initialize a Git repository with the contents of current working directory 
git init 

# ------------------------------------------------------
#  GitLab Remote Repo
# ------------------------------------------------------

# remove current remote repository (i.e. GitHub)
git remote remove origin

# connect local git to remote GitLab repo 
git remote add origin https://gitlab.com/suddharay/MyRepo1.git  

# check
git remote --verbose

# push entire local repo to remote repo on the web ....
# ensure that master branch in Gitlab is "unprotected" (generally protected by default) .. 
# change in settings in Gitlab
git push origin master --force

#------------------------------------------------------
#  Bitbucket Remote Repo
# ------------------------------------------------------

# remove current remote repository (i.e. GitHub or GitLab)
git remote remove origin

# connect local git to remote BitBucket repo 
git remote add origin https://bitbucket.org/ssray23/MyRepo1.git

# check
git remote --verbose

# remove SSL Verification -- this will prompt you for username and password 
# (Bitbucket) when you try to push 
git config --global http.sslVerify false

# push entire local repo to remote repo on the web
git push origin master --force

# remove current remote repository (i.e. BitBucket)
git remote remove origin