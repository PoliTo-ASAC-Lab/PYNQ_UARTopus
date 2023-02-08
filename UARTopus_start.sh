#!/bin/bash

if [ -z "$1" ]
  then
    echo "
    Usage: UARTopus_start.sh [N] - with N number of UARTs to open.
    "
    exit
fi

UART_b_adds=(
    "0x42C10000"
    "0x42C20000"
    "0x42C30000"
    "0x42C40000"
    "0x42C50000"
    "0x42C60000"
    "0x42C70000"
    "0x42C80000"
    "0x42C90000"
    "0x42CA0000"
    "0x42CB0000"
    "0x42C00000"
    )

# Set Session Name
SESSION="UARTopus"
SESSIONEXISTS=$(tmux list-sessions | grep $SESSION)

# Only create tmux session if it doesn't already exist
if [ "$SESSIONEXISTS" = "" ]
then
    python3 ./overlay_init.py
    
    # Start New Session with our name 
    tmux new-session -d -s $SESSION

    tmux set -g pane-border-status top
    tmux set -g pane-border-format "#{pane_title}"
    tmux set -g mouse on

    tmux rename-window -t 0 'UART_1-4'
    tmux split-window -v -t 0.0
    tmux split-window -h -t 0.0
    tmux split-window -h -t 0.2
    
    if [ $1 -gt 4 ]
    then
        tmux new-window -t $SESSION:1 -n 'UART_5-8'
        tmux split-window -v -t 1.0
        tmux split-window -h -t 1.0
        tmux split-window -h -t 1.2
    fi

    if [ $1 -gt 8 ]
    then
        tmux new-window -t $SESSION:2 -n 'UART_9-12'
        tmux split-window -v -t 2.0
        tmux split-window -h -t 2.0
        tmux split-window -h -t 2.2
    fi
    
    ##########################
    ######### Manual #########
    ##########################
    #tmux send-keys -t 0.0 'python3 ./main_server.py UART1 0x42C10000 3001' C-m
    #tmux select-pane -t 0.0 -T "UART1" # Setting title
    
    ##########################
    ######## Automatic #######
    ##########################
    for (( i = 0; i < $1; i++ )); do
        tmux send-keys -t $(($i/4)).$(($i%4)) "python3 ./main_server.py UART$(($i+1)) ${UART_b_adds[$i]} 300$(($i+1))" C-m
        tmux select-pane -t $(($i/4)).$(($i%4)) -T "UART$(($i+1))" # Setting title
    done

fi

tmux attach -t $SESSION:0.1