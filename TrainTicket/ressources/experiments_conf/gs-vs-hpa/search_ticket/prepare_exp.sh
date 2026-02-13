#!/bin/bash

source ./ressources/experiments_conf/gs-vs-hpa/search_ticket/global.conf

if [ ! -d ../global-ressources/load-profiles/tools/myenv ]; then
	python3 -m venv ../global-ressources/load-profiles/tools/myenv
fi

source "../global-ressources/load-profiles/tools/myenv/bin/activate"

pip3 install -r ../global-ressources/load-profiles/tools/pip3_modules_requirements.txt

if [[ ! -e $CONST_LOAD_FILE ]]; then
	python3 ../global-ressources/load-profiles/tools/gen_load_intensity_csv.py -g linear_perso --floor $PDS_MAX --ceil $PDS_MAX -t $DURATION_SECONDS -f $CONST_LOAD_FILE
fi

if [[ ! -e $LINEAR_LOAD_FILE ]]; then
	python3 ../global-ressources/load-profiles/tools/gen_load_intensity_csv.py -g linear_perso --floor 0 --ceil $PDS_MAX -t $DURATION_SECONDS -f $LINEAR_LOAD_FILE
fi

if [[ ! -e $SIN_LOAD_FILE ]]; then
	python3 ../global-ressources/load-profiles/tools/gen_load_intensity_csv.py -g sin --floor 0 --ceil $PDS_MAX -p $NB_STEPS -t $DURATION_SECONDS -f $SIN_LOAD_FILE
fi

if [[ ! -e $COS_LOAD_FILE ]]; then
	python3 ../global-ressources/load-profiles/tools/gen_load_intensity_csv.py -g cos --floor 0 --ceil $PDS_MAX -p $NB_STEPS -t $DURATION_SECONDS -f $COS_LOAD_FILE
fi

if [[ ! -e $STAIR_UP_LOAD_FILE ]]; then
	python3 ../global-ressources/load-profiles/tools/gen_load_intensity_csv.py -g stairsu --floor 0 --ceil $PDS_MAX -S $NB_STEPS -t $DURATION_SECONDS -f $STAIR_UP_LOAD_FILE
fi

if [[ ! -e $STAIR_DOWN_LOAD_FILE ]]; then
	python3 ../global-ressources/load-profiles/tools/gen_load_intensity_csv.py -g stairsd --floor 0 --ceil $PDS_MAX -S $NB_STEPS -t $DURATION_SECONDS -f $STAIR_DOWN_LOAD_FILE
fi


deactivate