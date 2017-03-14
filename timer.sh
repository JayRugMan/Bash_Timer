#!/bin/bash

### VERSION TRACKER #################################################################
# timer-v8.3.sh                                                                     #
#   - consolidated if statements in fMAIN to eliminate the need for SKIP_BIT        #
#                                                                                   #
# timer-v8.4.sh                                                                     #
#   - modified the usage of fHUMAN_READABLE_TIME to take arguments when called      #
#                                                                                   #
# timer-v8.5.sh                                                                     #
# - changed menu to list options vertically instead of horizontally                 #
# - changed fMAIN to clear the screen just after the read so that the menu is       #
#     presented after the category time outputs                                     #
# - added a just before closing to prevent the window from closing in a stand-      #
#     alone execution - Bug #2                                                      #
# - eliminate the need to display the last time because the screen clears           #
#     right after option selection                                                  #
#                                                                                   #
#####################################################################################

USER_ARG=${1}

fTIME_IN_SECONDS() {
	# Takes current time and echo's it back in "second" format
	# no input values needed if [ "${1}" == "-s" ]; then #new
	if [ "${USER_ARG}" == "--user-start-time" ] || [ "${USER_ARG}" == "-u" ]; then
		read -p " Please enter your start-time in 24 hour format (HH mm ss - no leading zeros)? " -e USER_HOURS USER_MIN USER_SEC
		TIME=(${USER_HOURS} ${USER_MIN} ${USER_SEC})
	else
		TIME_NOW=$(date +%H-%M-%S)
		TIME[0]=$(echo $TIME_NOW | awk -F '-' '{print $1}' | sed 's/^0*//')
		TIME[1]=$(echo $TIME_NOW | awk -F '-' '{print $2}' | sed 's/^0*//')
		TIME[2]=$(echo $TIME_NOW | awk -F '-' '{print $3}' | sed 's/^0*//')
	fi
	SEC=${TIME[2]}
	MIN_IN_SEC=$((TIME[1] * 60))
	HOUR_IN_SEC=$((TIME[0] * 3600))
	TOTAL_IN_SEC=$((HOUR_IN_SEC+MIN_IN_SEC+SEC))
	echo ${TOTAL_IN_SEC}
}

echo
START_TIME=$(fTIME_IN_SECONDS)
NOW_NOW=${START_TIME}
unset USER_ARG
HUMAN_TIME_OUT=" 0 Hour(s), 0 Minute(s), 0 Second(s)"
HUMAN_TIME_IN=0
TIME_STAMP=$(date +%H:%M:%S)
TIME_MARKER[0]=${NOW_NOW}
TIME_MARKER[1]=0
TM_SWITCH_a=0
TM_SWITCH_b=1
CALC_TIME_IN=''
CALC_TIME_OUT=''
SELECTION=0
CATEGORY_TIME=(0 0 0 0 0 0 0 0 0 0 0 0 0)
LOG_FILE=""
LOG_HEADING=""
NUM_CHECK='^[0-9]+$'

fMENU() {
	# Prints the header and main menu
	echo -e "\n \
1- Administration\t6-  Lab Time\t\t11- Training Dev\n \
2- Case Time\t\t7-  Meeting\t\t12- Training Received\n \
3- Consult\t\t8-  RCA\t\t\t13- Current Totals\n \
4- Development\t\t9-  Tools\t\t14- Summary and Quit\n \
5- KCS\t\t\t10- Training Del\n"
}

fCATEGORY_SELECT() {
	# fills arguments CATEGORY_TIME, LOG_FILE, LOG_HEADING and  based on selection SELECTION
	# input is SELECTION - returns full values above
	# usage: read -p " Selection: " -e SELECTION; fCATEGORY_SELECT
	case ${SELECTION} in
		1) # Administration
			LOG_FILE="Administration.out"
			LOG_HEADING="Administration"
			;;
		2) # Case Time
			LOG_FILE="CaseTime.out"
			LOG_HEADING="Case Time"
			;;
		3) # Consult
			LOG_FILE="Consult.out"
			LOG_HEADING="Consult"
			;;
		4) # Development
			LOG_FILE="Development.out"
			LOG_HEADING="Development"
			;;
		5) # KCS
			LOG_FILE="KCS.out"
			LOG_HEADING="KCS"
			;;
		6) # Lab Time
			LOG_FILE="LabTime.out"
			LOG_HEADING="Lab Time"
			;;
		7) # Meeting
			LOG_FILE="Meeting.out"
			LOG_HEADING="Meeting"
			;;
		8) # RCA
			LOG_FILE="RCA.out"
			LOG_HEADING="RCA"
			;;
		9) # Tools
			LOG_FILE="Tools.out"
			LOG_HEADING="Tools"
			;; 
		10) # Training Delivered
			LOG_FILE="TrainingDel.out"
			LOG_HEADING="Training Delivered"
			;;
		11) # Training Developed
			LOG_FILE="TrainingDev.out"
			LOG_HEADING="Training Developed"
			;;
		12) # Training Received
			LOG_FILE="TrainingRec.out"
			LOG_HEADING="Training Received"
			;;
		13) # allows you to see how much time you have accumulated for each category
			fCURRENT_TIMES
			;;
		14) # prints out a summary and exits the scripts
			fSUMMARY_AND_QUIT
			;;
		*) # anything other that 1 - 14 does nothing
			echo =e "\n Error, unknown selection, Please select 1 - 14"
			;;
	esac
}

fHUMAN_READABLE_TIME() { 
	# converts time in seconds back to hours minutes seconds
	# Input is HUMAN_TIME_IN - assignes argument HUMAN_TIME_OUT
	# usage: fHUMAN_READABLE_TIME <argument>
	HUMAN_TIME_IN=${1}
    if [ "${HUMAN_TIME_IN}" != '' ]; then
		((IN_HOURS=${HUMAN_TIME_IN}/3600))
		((IN_MINUTES=(${HUMAN_TIME_IN}%3600)/60))
		((IN_SECONDS=${HUMAN_TIME_IN}%60))
		HUMAN_TIME_OUT=" ${IN_HOURS} Hour(s), ${IN_MINUTES} Minute(s), ${IN_SECONDS} Second(s)"
	fi
}

fTIME_CALC() {
	# Calculates the difference in seconds between the two time markers
	# input is CALC_TIME_IN - assigns a calculated value to CALC_TIME_OUT
	# - determines the time difference, in seconds between the two time markers
	# - adds the time difference to the current CALC_TIME_OUT argument START_TIME=$(fTIME_IN_SECONDS)
	CALC_TIME_IN=${1}
    TIME_STAMP=$(date +%H:%M:%S) # records the time that this interval starts, to be used when the next interval is recorded
	NOW_NOW=$(fTIME_IN_SECONDS)
	TIME_MARKER[${TM_SWITCH_b}]=${NOW_NOW} # TM_SWITCH_b will start as 1 and become 0 at the end of each iteration of MAIN, unless skipped
	export TIME_DIFF=$((TIME_MARKER[${TM_SWITCH_b}] - TIME_MARKER[${TM_SWITCH_a}])) # _a will always be the earliest time, _b the most recent
	CALC_TIME_OUT=$((CALC_TIME_IN + TIME_DIFF))
}

fCURRENT_TIMES() {
# allows you to see how much time you have accumulated for each category
	SELECTION_HOLD=${SELECTION}
	HOLD_TIME_IN=${HUMAN_TIME_IN} # preserves current HUMAN_TIME_IN to preserve "Last Timestamp was:" 
	HOLD_TIME_OUT=${HUMAN_TIME_OUT} # preserves current HUMAN_TIME_OUT to preserve "Last Timestamp was:" 
	
    # displays current script duration in human readable time
	for i in {1..12}; do
		SELECTION=${i}; fCATEGORY_SELECT
		if [ -f "${LOG_FILE}" ]; then
			echo
			echo " ${LOG_HEADING}: "
			cat ${LOG_FILE}
			fHUMAN_READABLE_TIME ${CATEGORY_TIME[${SELECTION}]}
			echo " Total:   " ${HUMAN_TIME_OUT}
		fi
	done
	echo
    
	fHUMAN_READABLE_TIME $(($(fTIME_IN_SECONDS) - NOW_NOW))
    
    echo -e " Your total unused time is: \n"${HUMAN_TIME_OUT}
	echo
    
	fHUMAN_READABLE_TIME $(($(fTIME_IN_SECONDS) - START_TIME))
    
    echo -e " Your current total time is: \n"${HUMAN_TIME_OUT}
	SELECTION=${SELECTION_HOLD} # to avoid accumulating time on option 12
	HUMAN_TIME_IN=${HOLD_TIME_IN} # resets the preserved HUMAN_TIME for "Last Timestamp was:"
	HUMAN_TIME_OUT=${HOLD_TIME_OUT} # resets the preserved HUMAN_TIME for "Last Timestamp was:"
}

fSUMMARY_AND_QUIT() {
	# 
	FINAL_TIME=$(($(fTIME_IN_SECONDS) - START_TIME))
	
	# adds the final time to Administration time
	echo -n " "${TIME_STAMP} >> Administration.out
    
	fTIME_CALC ${CATEGORY_TIME[1]}
    CATEGORY_TIME[1]=${CALC_TIME_OUT}
	fHUMAN_READABLE_TIME ${TIME_DIFF}
    
	echo " "${HUMAN_TIME_OUT} >> Administration.out
	####
	
	clear
	echo -e "\n -- Time summary --\n"
	for i in {1..12}; do
		SELECTION=${i}; fCATEGORY_SELECT
		if [ -f "${LOG_FILE}" ]; then
			fHUMAN_READABLE_TIME ${CATEGORY_TIME[$SELECTION]}
			fLOG_TIME
		fi
	done
	
    fHUMAN_READABLE_TIME ${FINAL_TIME}
	LOG_HEADING=""
	LOG_FILE="TOTAL.out"
	echo " "$(date +%H:%M:%S)" "${HUMAN_TIME} >> ${LOG_FILE}
	fLOG_TIME
	cat ${TIME_LOG}
	echo
	echo
	read -p " Thanks for playing - hit enter to exit."
	echo
	
    
	exit 1
}

fLOG_TIME() {
	# Fills the time log with each time category total
	# inputs are LOG_FILE and LOG_HEADING - no value returned
	if [ -f ${LOG_FILE} ]; then
		echo >> ${TIME_LOG}
		echo ${LOG_HEADING} >> ${TIME_LOG}
		cat ${LOG_FILE} >> ${TIME_LOG}
		echo -e " Total- "${HUMAN_TIME_OUT} >> ${TIME_LOG}
		echo >> ${TIME_LOG}
		rm -f ${LOG_FILE}
	fi
}

fMAIN() {
    # Puts a header in the time log file
    clear
    echo -e "\n\t\t--- Jason's Time Tracker ---\n"
    TIME_LOG="Time_Log_$(date +%Y-%m-%d).txt"
    touch ${TIME_LOG} # creates the time log before main is run
    echo "__________________________________________________" >> ${TIME_LOG}
    echo " "$(date) >> ${TIME_LOG}
    
    #### MAIN PROGRAM ####
    while [ "${SELECTION}" != "14" ]; do
        fMENU
        read -p " Selection: " -e SELECTION
        clear # clears the screen for each header iteration
        echo -e "\n\t\t--- Jason's Time Tracker ---\n"
		fCATEGORY_SELECT
        
        if ! [[ ${SELECTION} =~ ${NUM_CHECK} ]] ; then
            echo " Error, unknown selection, must be numeric" >&2
        elif [ ${SELECTION} -gt 0 ] && [ ${SELECTION} -le 12 ]; then
            echo -n " ${TIME_STAMP}" >> "${LOG_FILE}"
            
            fTIME_CALC ${CATEGORY_TIME[${SELECTION}]}
            CATEGORY_TIME[${SELECTION}]=${CALC_TIME_OUT}
            fHUMAN_READABLE_TIME ${TIME_DIFF}
            
            echo " "${HUMAN_TIME_OUT}" ">> ${LOG_FILE}
            echo -e "\n "${LOG_HEADING}:" " ${HUMAN_TIME_OUT}
        
        # allows the array designations that is holding the time markers to switch places
            if [ ${TM_SWITCH_a} -eq 0 ]; then
                TM_SWITCH_a=1
                TM_SWITCH_b=0
            else
                TM_SWITCH_a=0
                TM_SWITCH_b=1
            fi
        fi
    done
}

fMAIN
