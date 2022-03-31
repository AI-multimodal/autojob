#!/bin/bash -l

# Changes directory to all directories listed in the first argument, and
# runs `sbatch submit.sbatch` in each of those directories if a particular
# file does not exist

NOW=$(date)

DIRECTORY=$(readlink -f "$1")  # Gets the absolute path
MAXJOBS="${2:-0}"
USER="${3:-mcarbone}"
DEPTH="${4:-1}"


file_list=$(find "$DIRECTORY" -mindepth "$DEPTH" -maxdepth "$DEPTH" -type d -exec echo {} \;)

if [ "$MAXJOBS" == 0 ]; then
    echo "dryrun - will submit submit.sbatch files in the following directories"
    for directory in $file_list; do
        echo "$directory"
    done
    exit 0
fi

function available_jobs {
    queued_or_running_jobs=$(squeue -u "$USER" | awk 'NR!=1' | wc -l)
    echo $((MAXJOBS - queued_or_running_jobs))
}

echo "$NOW"

if [ "$(available_jobs)" -lt 1 ]; then
    echo No jobs available to run - exiting
    echo
    exit
fi

currently_available_jobs="$(available_jobs)"
for directory in $file_list; do

    if [ "$currently_available_jobs" -le 0 ]; then
        break
    fi

    cd "$directory" || exit

    # If we already queued the job, we write that flag to the directory; we
    # should check for this and if the QUEUED file exists, we continue since
    # we don't want to submit the job multiple times
    if [ -e "QUEUED" ]; then
        continue
    fi

    if [ -e "submit.sbatch" ]; then
        slurm_out=$(sbatch submit.sbatch)
        if [[ "$slurm_out" =~ .*"Submitted batch job".* ]]; then
            job_id=${slurm_out##* }
            echo submitted job id "$job_id": "$directory"
            currently_available_jobs="$(available_jobs)"
        else
            echo submit error: "$slurm_out"
            continue
        fi
    elif [ -e "submit.sh" ]; then
        bash submit.sh
    else
        echo "Unknown error"
        exit 1
    fi

    touch "QUEUED"

    for (( ii=0; ii<"$DEPTH"; ii++ ))
    do
       cd ..
    done
done

cc=0
cctot=0
for directory in $file_list; do
    cctot=$((cctot+1))
    cd "$directory" || exit
    if [ -e "QUEUED" ]; then
        cc=$((cc+1))
    fi
    for (( ii=0; ii<"$DEPTH"; ii++ ))
    do
       cd ..
    done
done
remaining=$((cctot-cc))
echo jobs remaining: "$remaining"/"$cctot"
echo
