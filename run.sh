#!/bin/bash

if [[ -f .selected-mic ]]; then
    which=$(cat .selected-mic)
else
    echo "Finding microphones . . ."
    python stream/list-mics.py 2>/dev/null

    echo "Use which device?"
    read which
fi

echo "Selected microphone $which"

echo "Which mode? test|save|run"

read mode

if [[ $mode == 'test' ]]; then
    python stream/mic.py -s silvius-server.voxhub.io -d $which
elif [[ $mode == 'run' ]]; then
    python stream/mic.py -s silvius-server.voxhub.io -d $which | python grammar/main.py
elif [[ $mode == 'save' ]]; then
    echo "Choice saved to .selected-mic"
    echo $which >> .selected-mic
else
    echo "Unknown command $mode"
fi
