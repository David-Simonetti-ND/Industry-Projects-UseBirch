Before being able to run this software, the following steps are required
***GETTING INSTALLER***
Go to your home directory:
Type “wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh”
It will download a miniconda installer
***INSTALLING CONDA***
Run “bash Miniconda3-latest-Linux-x86_64.sh”
Press enter to continue
Press q to skip the license 
Type yes to begin install 
Press enter to confirm install to home directory
Type yes when it asks to initialize Miniconda
***CREATING ENVIRONMENT***
Type “bash” to have conda initialize
Type “conda create --name UseBirchEnv python=3.10”
This will create a conda environment called UseBirchEnv and install python version 3.10 in there.
Type y when it asks if it can download packages
Wait for it to download all the packages and create the environment
Type “conda activate UseBirchEnv”
Type “pip install pygdbmi”
***RUNNING trace.py***
Now navigate to a folder you want to clone the github repo to and clone the repo
cd into Industry-Projects-UseBirch
type "make update_gdb" in order to replace gdb with the new version
(gdb of at least 8.0 is required to run)
Typing “python3 trace.py” should now work!

***CONDA COMMANDS***
Typing “conda deactivate” will turn off the conda environment and return you to normal if you wish to work on something else
If you quit your ssh session, you will need to type “conda activate UseBirchEnv” will activate the environment we created and allow you to keep working on the project. Otherwise you will have no environment activate and not have access to python
Typing “conda install ‘PACKAGE_NAME’ ” or “pip install ‘PACKAGE_NAME’ “ will allow you to install additional packages if you need them

