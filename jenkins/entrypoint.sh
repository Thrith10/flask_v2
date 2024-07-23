#!/bin/sh
set -e

# Read secrets
JENKINS_USER=$(cat /run/secrets/jenkins_user)
JENKINS_PASS=$(cat /run/secrets/jenkins_pass)

# Export secrets as environment variables
export JENKINS_USER
export JENKINS_PASS

# Start Jenkins
exec /sbin/tini -- /usr/local/bin/jenkins.sh
