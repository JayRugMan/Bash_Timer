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
# timer-v8.6.sh                                                                     #
# - issue #3 display running totals always                                          #
#    - Changed option 13 to say "update unused/total"                               #
#    - Changed printed title of fCURRENT_TIMES                                      #
#    - Print fCURRENT_TIMES as program starts                                       #
#    - Print fCURRENT_TIMES for each option selected up to 13                       #
#    - Changed the Main title to be slimmer                                         #
#                                                                                   #
# timer-v8.7.sh                                                                     #
# - issue #8 cannot designate start time if not run from terminal                   #
#    - Removed USER_ARG                                                             #
#    - Created fUSER_TIME_CHECK function to ask user for a start time of continue   #
#      with the default time                                                        #
#    - Modified the fTIME_IN_SECONDS function to eliminate the if statement         #
#      as fUSER_TIME_CHECK takes care of user-designated time                       #
#    - Moved variable initialization to fMAIN due to fUSER_TIME_CHECK               #
#      dependencies                                                                 #
#    - Added PROGRAM_TITLE variable                                                 #
#                                                                                   #
# minor edit timer-v8.7-2                                                           #
#    - Changed the order of "Recorded Totals" and "Most Recent"                     #
#                                                                                   #
# timer-v8.8.sh                                                                     #
# - issue #12 Epoch Time Enhancement                                                #
#    - Eliminated the need for fTIME_IN_SECONDS                                     #
#    - Modified fHUMAN_READABLE_TIME to echo HUMAN_TIME_OUT                         #
#        - Track down dependencies of fHUMAN_READABLE_TIME as it currently stands   #
#                                                                                   #
# timer-v8.8-2                                                                      #
#  - Minor Edit =modified the date format from yyyy/mm/dd to yyyy-mm-dd do          #
#    that it works in MobaXterm on Windows operating systems                        #
#  - Replaced all \t with four spaces                                               #
#                                                                                   #
#####################################################################################

fUSER_TIME_CHECK() {
    # determines whether user wants to specify a start time or not
    echo -e "${PROGRAM_TITLE}\n"
    echo -e " To designate a start-time, enter it in 24 hour format\n \
(HH mm ss - no leading zeros) or just hit enter to continue"
    while [[ ! ${USER_HOURS} =~ ${NUM_CHECK} ]]; do
        read -p " : " -e USER_HOURS USER_MIN USER_SEC
        if [[ -z ${USER_HOURS} ]]; then
            START_TIME=$(date +%s)
            break
        fi
        TOTAL_IN_SEC=$(date --date="$(date +%Y-%m-%d) ${USER_HOURS:-0}:${USER_MIN:-0}:${USER_SEC:-0}" +%s)
        START_TIME=${TOTAL_IN_SEC}
    done
}

fMENU() {
    # Prints the header and main menu
    echo -e "\n \
1- Administration\t6-  Lab Time\t\t11- Training Dev\n \
2- Case Time\t\t7-  Meeting\t\t12- Training Received\n \
3- Consult\t\t8-  RCA\t\t\t13- Update Unused/Total Time\n \
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
            echo -e "\n Error, unknown selection, Please select 1 - 14"
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
    echo ${HUMAN_TIME_OUT}
}

fTIME_CALC() {
    # Calculates the difference in seconds between the two time markers
    # input is CALC_TIME_IN - assigns a calculated value to CALC_TIME_OUT
    # - determines the time difference, in seconds between the two time markers
    # - adds the time difference to the current CALC_TIME_OUT argument START_TIME=$(fTIME_IN_SECONDS)
    CALC_TIME_IN=${1}
    TIME_STAMP=$(date +%H:%M:%S) # records the time that this interval starts, to be used when the next interval is recorded
    NOW_NOW=$(date +%s)
    TIME_MARKER[${TM_SWITCH_b}]=${NOW_NOW} # TM_SWITCH_b will start as 1 and become 0 at the end of each iteration of MAIN, unless skipped
    export TIME_DIFF=$((TIME_MARKER[${TM_SWITCH_b}] - TIME_MARKER[${TM_SWITCH_a}])) # _a will always be the earliest time, _b the most recent
    CALC_TIME_OUT=$((CALC_TIME_IN + TIME_DIFF))
}

fCURRENT_TIMES() {
# allows you to see how much time you have accumulated for each category
    SELECTION_HOLD=${SELECTION}
    
    # displays current script duration in human readable time
    echo -ne "\n\t    == Recorded Totals =="
    
    for i in {1..12}; do
        SELECTION=${i}; fCATEGORY_SELECT
        if [ -f "${LOG_FILE}" ]; then
            echo
            echo " ${LOG_HEADING}: "
            cat ${LOG_FILE}
            echo " Total:   $(fHUMAN_READABLE_TIME ${CATEGORY_TIME[${SELECTION}]})"
        fi
    done
    
    echo -e "\n Your total unused time is: \n$(fHUMAN_READABLE_TIME $(($(date +%s) - NOW_NOW)))\n"
    echo -e " Your current total time is: \n$(fHUMAN_READABLE_TIME $(($(date +%s) - START_TIME)))"
    SELECTION=${SELECTION_HOLD} # to avoid accumulating time on option 12
}

fSUMMARY_AND_QUIT() {
    # 
    FINAL_TIME=$(($(date +%s) - START_TIME))
    
    # adds the final time to Administration time
    echo -n " "${TIME_STAMP} >> Administration.out
    
    fTIME_CALC ${CATEGORY_TIME[1]}
    CATEGORY_TIME[1]=${CALC_TIME_OUT}
    
    echo " $(fHUMAN_READABLE_TIME ${TIME_DIFF})" >> Administration.out
    ####
    
    clear
    echo -e "\n -- Time summary --\n"
    for i in {1..12}; do
        SELECTION=${i}; fCATEGORY_SELECT
        if [ -f "${LOG_FILE}" ]; then
            fLOG_TIME "$(fHUMAN_READABLE_TIME ${CATEGORY_TIME[$SELECTION]})"
        fi
    done
    
    LOG_HEADING=""
    LOG_FILE="TOTAL.out"
    FINAL_HUMAN_READABLE_TIME=$(fHUMAN_READABLE_TIME ${FINAL_TIME})
    echo " $(date +%H:%M:%S) ${FINAL_HUMAN_READABLE_TIME}" >> ${LOG_FILE} 
    fLOG_TIME "${FINAL_HUMAN_READABLE_TIME}"
    cat ${TIME_LOG}
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
        echo -e " Total-   ${1}" >> ${TIME_LOG}
        echo >> ${TIME_LOG}
        rm -f ${LOG_FILE}
    fi
}

fMAIN() {
    NUM_CHECK='^[0-9]+$'
    PROGRAM_TITLE="================== Jason's Time Tracker ========="
    # Sets up the initial variables
    fUSER_TIME_CHECK

    ## set Variables ##
    NOW_NOW=${START_TIME}
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

    clear
    echo -e "${PROGRAM_TITLE}"
    TIME_LOG="Time_Log_$(date +%Y-%m-%d).txt"
    touch ${TIME_LOG} # creates the time log before main is run
    echo "__________________________________________________" >> ${TIME_LOG}
    echo " "$(date) >> ${TIME_LOG}
    fCURRENT_TIMES
    
    #### MAIN PROGRAM ####
    while [ "${SELECTION}" != "14" ]; do
        fMENU
        read -p " Selection: " -e SELECTION
        clear # clears the screen for each header iteration
    echo -e "${PROGRAM_TITLE}"
        fCATEGORY_SELECT
        
        if ! [[ ${SELECTION} =~ ${NUM_CHECK} ]] ; then
            echo " Error, unknown selection, must be numeric" >&2
        elif [ ${SELECTION} -gt 0 ] && [ ${SELECTION} -le 12 ]; then
            echo -n " ${TIME_STAMP}" >> "${LOG_FILE}"
            
            fTIME_CALC ${CATEGORY_TIME[${SELECTION}]}
            CATEGORY_TIME[${SELECTION}]=${CALC_TIME_OUT}
            TIME_OUTPUT=$(fHUMAN_READABLE_TIME ${TIME_DIFF}) # TIME_DIFF is global and assigned in fTIME_CALC
            SELECTION_OUTPUT=$(echo -e "\n\t    == Most Recent ==\n ${LOG_HEADING}: ${TIME_OUTPUT}")
            
            echo " ${TIME_OUTPUT} ">> ${LOG_FILE} 
            echo "${SELECTION_OUTPUT}"
            
            fCURRENT_TIMES
        
        # allows the array designations that are holding the time markers to switch places
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
