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
#  - Minor Edit - modified the date format from yyyy/mm/dd to yyyy-mm-dd do         #
#    that it works in MobaXterm on Windows operating systems                        #
#  - Replaced all \t with four spaces                                               #
#                                                                                   #
# timer-v8.9                                                                        #
#  - Issue #5, arguments, not files                                                 #
#    - created an array to hold each category's output                              #
#    - restructured fCATEGORY_SELECT, fCURRENT_TIMES, fSUMMARY_AND_QUIT and         #
#      fMAIN to accomodate the time arrays instead of files                         #
#    - eliminated the need for fLOG_TIME                                            #
#    - added comments to explain each line of code                                  #
#                                                                                   #
# timer-v8.10                                                                       #
#  - Issue #16, Let the user define the categories                                  #
#    - created timer.conf to give the user the ability to fill with their own       #
#      categories                                                                   #
#    - created fSET_SPACES which intakes categories and determines formatting       #
#    - modified fMAIN and fMENU to accomodate timer.conf and fSET_SPACES            #
#    - modified fCATEGORY_SELECT, fCURRENT_TIMES, and fSUMMARY_AND_QUIT to work     #
#      with dynamic categories                                                      #
#    - modified fCATEGORY_SELECT to take an argument instead of using global        #
#    - changes created redundant selection checking which will need to be           #
#      corrected in the next version                                                #
#                                                                                   #
#####################################################################################

fUSER_TIME_CHECK() {
    # determines whether user wants to specify a start time or not
    # and sets START_TIME (in seconds) accordingly
    echo -e "${PROGRAM_TITLE}\n"
    echo -e " To designate a start-time, enter it in 24 hour format\n \
    \b\b\b\b(HH mm ss - no leading zeros) or just hit enter to continue"
    while [[ ! ${USER_HOURS} =~ ${NUM_CHECK} ]]; do # Checks that the input is a number and loops if not
        read -p " : " -e USER_HOURS USER_MIN USER_SEC
        if [[ -z ${USER_HOURS} ]]; then # if no time is specified, start time is set to "now" and the loop breaks
            START_TIME=$(date +%s)
            break
        fi
        TOTAL_IN_SEC=$(date --date="$(date +%Y-%m-%d) ${USER_HOURS:-0}:${USER_MIN:-0}:${USER_SEC:-0}" +%s)
        START_TIME=${TOTAL_IN_SEC}
    done
}

fSET_SPACES() {
    ## usage:
    ## fSET_SPACES $categoryIndexes CAT_HEADING_ARRAY[@]
    unset menuOut
    
    ## takes categories in timer.config, numbers them, and
    ## loads them into an output array
    catNum=${1}
    categoryArray=("${!2}")
    for i in $(seq 0 $catNum); do
        menuOut[$i]=" $((i+1))- ${categoryArray[$i]}"
    done
    menuOut[$((catNum+1))]=" r- Refresh"
    # menuOut[$((catNum+2))]=" a- Add Category" ## JH future development
    menuOut[$((catNum+2))]=" q- Summary and Quit"
    
    ## determines which menu item is the longest
    spaceArrayInc=0; finalArg=0; for i in "${menuOut[@]}"; do
        testArg=$(echo "${i}" | wc -c)
        if [[ ${testArg} -gt ${finalArg} ]]; then
            finalArg=${testArg}
        fi
    done; unset testArg
    
    ## determines the white space after each menu
    ## item based on the logest menu item
    spaceArrayInc=0; for i in "${menuOut[@]}"; do
        menuItemSpacing[${spaceArrayInc}]=$(((finalArg) - $(echo "${i}" | wc -c)))
        ((spaceArrayInc++))
    done; unset spaceArrayInc finalArg
    
    ## adds the trailing spaces to the menu items
    spaceArrayInc=0; for i in "${menuItemSpacing[@]}"; do
        for j in `seq 1 ${i}`; do
            MenuItemSpaced[${spaceArrayInc}]="${MenuItemSpaced[${spaceArrayInc}]} "
        done
        menuOut[${spaceArrayInc}]="${menuOut[${spaceArrayInc}]} ${MenuItemSpaced[${spaceArrayInc}]}" ## used as a global array
        ((spaceArrayInc++))
    done
    unset spaceArrayInc catNum categoryArray menuItemSpacing MenuItemSpaced
}

fMENU() {
    # Prints the main menu
    # uses menuOut from fSET_SPACES
    menuArray=("${menuOut[@]}")
    echo
    for i in {0..4}; do
        printf "%s%s%s%s\n" "${menuArray[${i}]}" "${menuArray[$((i+5))]}" "${menuArray[$((i+10))]}" "${menuArray[$((i+15))]}"
    done
    echo
}

fCATEGORY_SELECT() {
    # fills arguments CATEGORY_TIME, LOG_FILE, LOG_HEADING and  based on selection selection
    # input is selection - returns full values above
    # usage: read -p " Selection: " -e selection; fCATEGORY_SELECT ${selection}
    selection=${1}
    case ${selection} in
        r) # allows you to see how much time you have accumulated for each category
            fCURRENT_TIMES
            ;;
        q) # prints out a summary and exits the scripts
            fSUMMARY_AND_QUIT
            ;;
        *) # error handling in fMAIN... will fix in later version ## JH 
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
    # usage: fTIME_CALC <argument>
    # defines global variables TIME_STAMP, NOW_NOW, TIME_DIFF and CALC_TIME_OUT
    # - determines the time difference, in seconds between the two time markers
    # - adds the time difference to the current CALC_TIME_OUT argument
    CALC_TIME_IN=${1}
    TIME_STAMP=$(date +%T) # records the time that this interval starts, to be used when the next interval is recorded
    NOW_NOW=$(date +%s)
    TIME_MARKER[${TM_SWITCH_b}]=${NOW_NOW} # TM_SWITCH_b will start as 1 and become 0 at the end of each iteration of MAIN, unless skipped
    TIME_DIFF=$((TIME_MARKER[${TM_SWITCH_b}] - TIME_MARKER[${TM_SWITCH_a}])) # _a will always be the earliest time, _b the most recent
    CALC_TIME_OUT=$((CALC_TIME_IN + TIME_DIFF))
}

fCURRENT_TIMES() {
    # allows you to see how much time you have accumulated for each category
    # and the current script duration in human readable time
    # uses global variable LOG_ARRAY, LOG_ARRAY, CATEGORY_TIME, NOW_NOW, and START_TIME
    # only displays information
    echo -ne "\n\t    == Recorded Totals =="
    for i in `seq 0 ${categoryIndexes}`; do 
        if [ ! -z "${LOG_ARRAY[${i}]}" ]; then
            echo
            echo -n " ${CAT_HEADING_ARRAY[${i}]}: "
            echo -e "${LOG_ARRAY[${i}]}"
            echo -e "   Total:   $(fHUMAN_READABLE_TIME ${CATEGORY_TIME[${i}]})"
        fi
    done
    echo -e "\n Your total unused time is:\n   $(fHUMAN_READABLE_TIME $(($(date +%s) - NOW_NOW)))\n"
    echo -e " Your current total time is:\n   $(fHUMAN_READABLE_TIME $(($(date +%s) - START_TIME)))"
}

fSUMMARY_AND_QUIT() {
    # calculates the final time
    FINAL_TIME=$(($(date +%s) - START_TIME))
    ####
    ####
    # adds the final time to category 1
    TIME_STAMP_HOLD="${TIME_STAMP}"
    fTIME_CALC ${CATEGORY_TIME[0]}
    CATEGORY_TIME[0]=${CALC_TIME_OUT}
    TIME_OUTPUT=$(fHUMAN_READABLE_TIME ${TIME_DIFF}) # TIME_DIFF is global and assigned in fTIME_CALC
    LOG_ARRAY[0]=" ${LOG_ARRAY[0]}\n   ${TIME_STAMP_HOLD} ${TIME_OUTPUT} "
    ####
    ####
    # iterates through the time history of each category and logs it into TIME_LOG
    clear
    echo -e "\n -- Time summary --\n"
    for i in `seq 0 ${categoryIndexes}`; do 
        if [ ! -z "${LOG_ARRAY[${i}]}" ]; then
            echo -ne "\n ${CAT_HEADING_ARRAY[${i}]}" >> ${TIME_LOG}
            echo -e "${LOG_ARRAY[${i}]}" >> ${TIME_LOG}
            echo -e "   Total-   $(fHUMAN_READABLE_TIME ${CATEGORY_TIME[${i}]})" >> ${TIME_LOG}
        fi
    done
    ####
    ####
    # logs total time, prints out TIME_LIOG, and waits for user input before exiting with status 0
    FINAL_HUMAN_READABLE_TIME=$(fHUMAN_READABLE_TIME ${FINAL_TIME})
    LOG_ARRAY[${numOfCategories}]=$(echo " $(date +%H:%M:%S) ${FINAL_HUMAN_READABLE_TIME}")
    echo -e "\n\n Total- ${FINAL_HUMAN_READABLE_TIME}\n\n" >> ${TIME_LOG}
    cat ${TIME_LOG}
    read -p " Thanks for playing - hit enter to exit."
    echo
    exit 0
}

fMAIN() {
    ## set Variables ##
    NUM_CHECK='^[0-9]+$'
    PROGRAM_TITLE="================== Jason's Time Tracker ========="
    fUSER_TIME_CHECK # Sets up the initial variables
    NOW_NOW=${START_TIME}
    HUMAN_TIME_OUT=" 0 Hour(s), 0 Minute(s), 0 Second(s)"
    HUMAN_TIME_IN=0
    TIME_STAMP=$(date +%T)
    TIME_MARKER[0]=${NOW_NOW}
    TIME_MARKER[1]=0
    TM_SWITCH_a=0
    TM_SWITCH_b=1
    CALC_TIME_IN=''
    CALC_TIME_OUT=''
    selection=0
    source timer.conf || echo -e "\n Error, could not find timer.conf\n" 
    numOfCategories=${#CAT_HEADING_ARRAY[@]}
    categoryIndexes=$((numOfCategories - 1))
    for i in `seq 0 $categoryIndexes`; do CATEGORY_TIME[$i]=0; done
    fSET_SPACES ${categoryIndexes} CAT_HEADING_ARRAY[@]
    ####
    ####
    # clears the screen, prints the title and creates the TIME_LOG file
    clear
    echo -e "${PROGRAM_TITLE}"
    TIME_LOG="Time_Log_$(date +%Y-%m-%d).txt"
    touch ${TIME_LOG} # creates the time log before main is run
    echo "__________________________________________________" >> ${TIME_LOG}
    echo " "$(date) >> ${TIME_LOG}
    ####
    ####
    # loops as long as the selection does not equal q
    while [ "${selection}" != "q" ]; do
        # prints the menu, waits for option selection, clears the screen,
        # prints the title, and runs category check
        fMENU
        read -p " Selection: " -e selection
        clear # clears the screen for each header iteration
        echo -e "${PROGRAM_TITLE}" 
        fCATEGORY_SELECT ${selection}
        if [[ ${selection} == "r" ]] ; then
            continue
        ####
        ####
        # prints an error if the selection is non-numeric and loops again
        # without doing anything else
        elif ! [[ ${selection} =~ ${NUM_CHECK} ]] ; then
            echo " Error, unknown selection" >&2
        ####
        ####
        # makes sure the selection is in range and continues if it is or
        # loops agian if not
        elif [ ${selection} -gt 0 ] && [ ${selection} -le ${numOfCategories} ]; then
            # passes the old timestamp to a hold variable because TIME_CALC redefines it
            # and updates the total for the category selected
            TIME_STAMP_HOLD="${TIME_STAMP}"
            fTIME_CALC ${CATEGORY_TIME[$((selection - 1))]}
            CATEGORY_TIME[$((selection - 1))]=${CALC_TIME_OUT}
            ####
            ####
            # creates human readable output, stacks it in that category's output array, 
            # prints that catogory's accumulated human-readable output, and prints the 
            # current totals for all categories
            TIME_OUTPUT=$(fHUMAN_READABLE_TIME ${TIME_DIFF}) # TIME_DIFF is global and assigned in fTIME_CALC
            SELECTION_OUTPUT=$(echo -e "\n\t    == Most Recent ==\n ${CAT_HEADING_ARRAY[$((selection - 1))]}: ${TIME_OUTPUT}")
            LOG_ARRAY[$((selection - 1))]=" ${LOG_ARRAY[$((selection - 1))]}\n   ${TIME_STAMP_HOLD} ${TIME_OUTPUT} "
            echo "${SELECTION_OUTPUT}"
            fCURRENT_TIMES
            ####
            ####
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
