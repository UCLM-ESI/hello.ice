#!/bin/bash

tmux -f .tmux.conf new-session -d -s session
tmux -f .tmux.conf split-window -h
tmux -f .tmux.conf split-window -v
tmux -f .tmux.conf send-keys -t session:0.0 "make start && make run-publisher" C-m
tmux -f .tmux.conf send-keys -t session:0.1 "make run-subscriber" C-m
tmux -f .tmux.conf send-keys -t session:0.2 "make run-subscriber" C-m
tmux -f .tmux.conf attach-session -t session
