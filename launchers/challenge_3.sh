#!/bin/bash

source /environment.sh

# initialize launch file
dt-launchfile-init

# launch subscriber
dt-exec python3 "$DT_REPO_PATH/packages/challenge_3_solution/camera_reader_node.py" &
dt-exec python3 "$DT_REPO_PATH/packages/challenge_3_solution/control_lane_node.py"

# wait for app to end
dt-launchfile-join