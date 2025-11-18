#!/bin/bash

tmux new-session -d -s session

tmux set-option -g mouse on
tmux setw -g monitor-activity on
tmux set-option -g visual-activity on
tmux bind-key x kill-session
tmux set-option -g set-titles off

tmux split-window -h
tmux split-window -v

tmux send-keys -t session:0.0 "make start && make run-publisher" C-m
tmux send-keys -t session:0.1 "make run-subscriber" C-m
tmux send-keys -t session:0.2 "make run-subscriber" C-m

tmux attach-session -t session
