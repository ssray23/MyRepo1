# -------------------------------------------------------------------------------------------
#  GitHub Remote Repo (should always be kept up to date first before GitLab and Bitbucket)
# -------------------------------------------------------------------------------------------
# switch to folder where you want your repos to be 
cd /c/suddha/GitRepos

# clone a remote repo 
# !! CAUTION !! - ONLY clone if starting on a clean new system where MyRepo1 folder does not exists)
git clone https://github.com/ssray23/MyRepo1.git

# Get inside your repo where you did all the new programming
cd /c/suddha/GitRepos/MyRepo1/

# Initialize local Git repository with the contents of current working directory 
git init 

# check status of contents in the repository
git status

# EXAMPLE ONLY - How to add a single file i.e. FileA in the directory to the repository
git add FileA

# EXAMPLE ONLY - How to add a single file in a folder i.e. add FileB inside Folder1 to the repository
git add Folder1/FileB

# EXAMPLE ONLY - How to add entire Folder2 to the repository
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
git commit -m "Replace with what changes you did i.e. new Java Web App?"

# check git remote (i.e. repo on github)
git remote --verbose

# remove current remote repository (i.e. GitHub or GitLab) .. just in case
git remote remove origin

# connect local git to remote github repo (you will get fatal error if already linked to remote)
git remote add origin https://github.com/ssray23/MyRepo1.git

# push to remote repo on the web
git push -u origin master

# Remote GitHub MyRepo1 is now in SYNC with your local Git Repo 
# Force Push everything in the local Git repo to your remote GitLab and Bitbucket Repos
# Run the below shell script to invoke the script
./git_force_push_all_to_bitbucket_gitlab.sh

