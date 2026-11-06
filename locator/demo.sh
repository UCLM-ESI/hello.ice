#!/bin/bash

WAIT_REGISTRY="while ! bash -c ':> /dev/tcp/127.0.0.1/4061' 2>/dev/null; do sleep 0.5; done"

mkdir -p /tmp/icedata/registry

tmux new-session -d -s session

tmux set-option -g mouse on
tmux setw -g monitor-activity on
tmux set-option -g visual-activity on
tmux bind-key x kill-session
tmux set-option -g set-titles off

tmux split-window -h
tmux split-window -v -t session:0.1

tmux send-keys -t session:0.0 "icegridregistry --Ice.Config=registry.config" C-m
tmux send-keys -t session:0.1 "$WAIT_REGISTRY" C-m "./server.py --Ice.Config=server.config" C-m
tmux send-keys -t session:0.2 "$WAIT_REGISTRY; sleep 1" C-m "./client.py --Ice.Config=locator.config printer1@PrinterAdapter1" C-m

tmux attach-session -t session

tmux kill-session -t session 2>/dev/null
pkill -f "icegridregistry --Ice.Config=registry.config"
