#! /bin/bash

# Clear workspace
clear

# Load Configs
source lib/diverseShell.config
source project.config

# Set custom messages
BAD="${bLRed}${fBlack}[\xE2\x9C\x98]${dsRE}"
GOOD="${bLGreen}${fBlack}[\xE2\x9C\x94]${dsRE}"
WARN="${bLYellow}${fBlack}[\xE2\x80\xBC]${dsRE}"
LOAD="${bLBlue}${fBlack}[\xE2\x86\xBB]${dsRE}"

# Super-cool logo
read -r -d '' LOGO << EOM
._____.               ._.       ._____._.
|  |  |_______________|_|_______|  _  |_|
|     | | |     |     | |   | . |   __| |
|__|__|___|_|_|_|_|_|_|_|_|_|_  |__|  |_|
                            |___|  
EOM

printf "${fCyan}${LOGO}${dsRE}\n"

# HummingPi - Main Structure
if [ "${projectType}" = "java" ]; then
	# Create Variables for Project
	projectFile="${projectName}.java"
	projectBuildDir="java/build"
	projectSourceDir="java/src"
	# Debugging Title
	printf "${fMagenta}Debugging:${dsRE}\n"

	# Check if Project Exists
	if [ ! -f "${projectSourceDir}/${projectFile}" ]; then
		printf "${fWhite}Project Not Found ${BAD}\n"
		exit 1
	else
		printf "${fWhite}Project Found ${GOOD}\n"
	fi

	# Check if Source Directory Exists
	if [ -d "$projectSourceDir" ]; then
		printf "${fWhite}Source Directory exists ${GOOD}\n"
		# Check if Build directory exists (and create one if it doesn't)
		if [ -d "$projectBuildDir" ]; then
			printf "${fWhite}Build Directory ${GOOD}\n"
		else
			printf "${fWhite}Build Directory Missing ${WARN}\n"
			printf "${fWhite}Creating Build Directory ${LOAD}\n"
			mkdir -p "${projectBuildDir}"
			printf "${fWhite}Build Directory Created ${GOOD}\n"
		fi
		# Debugging Title
		printf "${fMagenta}Intializing:${dsRE}\n"
		COMPILE=$(javac -classpath :java/assets/libs/hummingbird.jar java/src/${projectFile})
		RUNJAVA=$(java -classpath java/assets/libs/hummingbird.jar: ${projectName})
		if [ "$COMPILE" ]; then
			printf "${fWhite}Project Compiled ${GOOD}\n"
		fi
		mv java/src/"${projectName}".class .
		if [ "$RUNJAVA" ]; then
			printf "${fWhite}Project Ran ${GOOD}\n"
		else
			printf "${fWhite}Project Can't Run ${BAD}\n"
		fi
	else
		printf "${fWhite}Source Directory Missing ${BAD}\n"
		exit 1
	fi
elif [ "${projectType}" = "python" ]; then
	projectFile="${projectName}.py"
	printf "${fMagenta}HummingPi will work for Python, eventually. Stay Tuned!${dsRE}\n"
	exit 1
else
	printf "[${dsU}${projectType}${dsRE}] is not supported by HummingPi ${BAD}\n"
	exit 1
fi
