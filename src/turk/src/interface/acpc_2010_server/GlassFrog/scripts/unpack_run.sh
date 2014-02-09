#!/bin/bash

AGENT_PACKAGE=foo.tgz
AGENT_SUBDIR=foo/

AGENT_SUBMISSION_DIR=./
AGENT_EXECUTION_DIR=../current_agent/

# Remove previous agent data
rm -rf $AGENT_EXECUTION_DIR/*

#Extract agent from submission
tar -C $AGENT_EXECUTION_DIR -xzvf $AGENT_SUBMISSION_DIR/$AGENT_PACKAGE

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
