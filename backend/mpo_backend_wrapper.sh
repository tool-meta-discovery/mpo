#!/bin/sh

trap 'trap " " SIGTERM; kill 0; wait' SIGINT SIGTERM

conda run --no-capture-output -n mpo python parallel_service.py 1>parallel_service.out  & 
conda run --no-capture-output -n mpo waitress-serve --call app:create_app 1>waitress.out  &
echo 'Both process have been started, see .out files for logs. Errors will show up here'
# Wait for any process to exit
wait 

# Exit with status of process that exited first
exit $?