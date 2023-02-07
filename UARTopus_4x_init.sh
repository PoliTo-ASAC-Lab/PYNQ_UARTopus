#!/bin/sh

python3 ./overlay_init.py

# Set Session Name
SESSION="UARTopus"
SESSIONEXISTS=$(tmux list-sessions | grep $SESSION)

# Only create tmux session if it doesn't already exist
if [ "$SESSIONEXISTS" = "" ]
then
    # Start New Session with our name 
    tmux new-session -d -s $SESSION

    tmux rename-window -t 0 'UARTs'
    tmux split-window -v -t 0.0
    tmux split-window -h -t 0.0
    tmux split-window -h -t 0.2

    tmux new-window -t $SESSION:1 -n 'scratch'
    tmux send-keys -t 0.0 'python3 ./main_server.py UART1 0x42C10000 3001' C-m
    tmux send-keys -t 0.1 'python3 ./main_server.py UART2 0x42C20000 3002' C-m
    tmux send-keys -t 0.2 'python3 ./main_server.py UART3 0x42C30000 3003' C-m
    tmux send-keys -t 0.3 'python3 ./main_server.py UART4 0x42C40000 3004' C-m

    tmux new-window -t $SESSION:2 -n 'UART_2'
    tmux send-keys -t 'UART_2' 'echo ciaooooDNE' C-m
fi

# Attach Session, on the Main window
tmux attach -t $SESSION:0.1


# select-pane -t paneIndexInteger -T "fancy pane title"
# select-pane -t paneIndexInteger -T "fancy pane title"
# select-pane -t paneIndexInteger -T "fancy pane title"
# select-pane -t paneIndexInteger -T "fancy pane title"
# select-pane -t paneIndexInteger -T "fancy pane title"