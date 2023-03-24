#!/bin/bash
################################################################################
# Script to handle python environment and startup given script
################################################################################

################################################################################
# Set base variables, you may tweak here
################################################################################
# Set name of python environment
ENV_NAME="venv"
# Set name of python environment list exported by pip freeze > ${REQ_NAME}
REQ_NAME="requirements.txt"
# Get name of script to start
SCRIPT=$(basename "$1")
# Set default name of script to run
DEF_SCRIPT="program.py"

################################################################################
# Set internal variables, don't touch unless you know what you're doing!
################################################################################
# Get startup path of script
PATH_BASE=$(dirname "$0")
# Set FQN of environment
PATH_ENVIRONMENT="${PATH_BASE}/${ENV_NAME}"

################################################################################
# Check environment for existence
################################################################################
if [[ ! -d "${PATH_ENVIRONMENT}" ]]; then
    # Create environment
    echo "Create missing environment [${ENV_NAME}]"
    python -m venv ${ENV_NAME}

    # Activate environment
    if [[ -z "${VIRTUAL_ENV}" ]]; then
        echo "Initial activation of environment [${ENV_NAME}]"
        source "${PATH_ENVIRONMENT}/bin/activate"
    fi

    # Install required modules
    if [[ -f "${REQ_NAME}" ]]; then
        echo "Install required modules from [${REQ_NAME}] to [${ENV_NAME}]"
        cat ${REQ_NAME}
        pip install -r ${REQ_NAME}
    else
        echo "List of required modules [${REQ_NAME}] not found"
    fi
fi

################################################################################
# Activate environment if not already done
################################################################################
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "Activate environment [${ENV_NAME}]"
    source "${PATH_ENVIRONMENT}/bin/activate"
fi

################################################################################
# Determine script to run; if no name is passed, use default
################################################################################
if [[ -z "${SCRIPT}" ]]; then
    SCRIPT="${DEF_SCRIPT}"
fi

################################################################################
# Execute script
################################################################################
if [[ -f ${SCRIPT} ]]; then
    echo "Execute script [${SCRIPT}]"
    python ${SCRIPT}
else
    echo "Script [${SCRIPT}] not found :-("
fi
