#!/bin/bash

# This can be used to more quickly startlarge agent as files don't need to be
# copied.  As long as the location of the real files does not have write
# permissions (potentially using a different user to run the agent than the
# user who owns the files) then you won't have competitors stomping their
# submissions.  The only caveat being that if they try to write to an already
# existing file: this will fail.

AGENT_SUBMISSION_DIR=/home/acpc/submissions/2p_limit/
AGENT_SUBDIR=foo/

AGENT_EXECUTION_DIR=/home/agent/current_agent

# Remove previous agent data
rm -rf $AGENT_EXECUTION_DIR/*

# Create symlinks to existing agent directory structure
# NOTE: This script requires that the agent subdirectory is a subdirectory of
# the directory containing the script
find $AGENT_SUBDIR/ -type d -exec mkdir $AGENT_EXECUTION_DIR/'{}' \;
find $AGENT_SUBDIR/ -type f -exec ln -s $AGENT_SUBMISSION_DIR/'{}' $AGENT_EXECUTION_DIR/'{}' \;

# Change directory into the agent's directory and execute their startme script
cd $AGENT_EXECUTION_DIR/$AGENT_SUBDIR
./startme.sh $1 $2 &

# Kill agents that aren't exiting correctly once the match is over
pid=$!
pgid=`ps -eo pid,pgid | grep $pid | perl -ne 'split; print $_[1];'`
while kill -s 0 $pid; do
  sleep 5
  if netstat -n | grep $1:$2 | grep -q CLOSE_WAIT; then kill -9 -$pgid; fi
done
