"""
This module contains functions for running calculations using different packages.
It provides functions for running calculations with GAMESS US and NWChem.
The module also includes functions for handling job status, file upload, and cleanup.
"""
import logging
import subprocess
import threading

from ivette.file_io_module import (
    convert_xyz_to_sdf,
    extract_geometries
)

from .IO_module import (
    get_cpu_core_count,
    setUp,
    cleanUp,
    check_gamess_installation,
    is_nwchem_installed,
    waiting_message,
    print_color
)

from .supabase_module import (
    downloadFile,
    update_job,
    uploadFile,
    insertSpecies
)

# Info disabling
logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("aiohttp").setLevel(logging.CRITICAL)
logging.getLogger("gql").setLevel(logging.CRITICAL)

# Create a flag to signal when the job is done
job_done = False
job_failed = False
operation = None


def run_rungms(job_id, nproc):
    """
    Run the 'rungms' command with the given id and number of processors.

    Args:
        id (str): The id of the command.
        nproc (int): The number of processors to use.

    Raises:
        subprocess.CalledProcessError: If the 'rungms' command returns a non-zero exit code.

    Returns:
        None
    """
    global job_done
    global job_failed

    command = ["rungms tmp/" + job_id + " 00 " +
               str(nproc)]  # The last one is ncores

    with open(f"tmp/{job_id}.out", "w", encoding='utf-8') as output_file:
        try:

            # Run the 'rungms' command and wait for it to complete
            subprocess.run(
                command,
                stdout=output_file,
                stderr=subprocess.STDOUT,
                shell=True,
                check=True,  # This will raise an error if the command returns a non-zero exit code
            )

            uploadFile(f"{job_id}.out", job_id, "Calculation/", localDir="tmp/")
            update_job(job_id, nproc=0)
            job_done = True

        except subprocess.CalledProcessError as e:
            if not e.returncode == -2:

                update_job(job_id, "failed", nproc=0)
                uploadFile(f"{job_id}.out", job_id, "Calculation/", localDir="tmp/")

            cleanUp(job_id)
            print(f"\n Job failed with exit code {e.returncode}.")
            job_done = True
            job_failed = True


def run_nwchem(job_id, nproc):
    """
    Run the calculation
    """

    global job_done
    global job_failed

    if nproc:

        command = [
            f"mpirun -np {nproc} --use-hwthread-cpus $NWCHEM_TOP/bin/$NWCHEM_TARGET/nwchem tmp/{job_id}"]

    else:

        command = [
            f"mpirun -map-by core --use-hwthread-cpus $NWCHEM_TOP/bin/$NWCHEM_TARGET/nwchem tmp/{job_id}"]

    with open(f"tmp/{job_id}.out", "w", encoding='utf-8') as output_file:
        try:

            # Run the 'rungms' command and wait for it to complete
            subprocess.run(
                command,
                stdout=output_file,
                stderr=subprocess.STDOUT,
                shell=True,
                check=True,  # This will raise an error if the command returns a non-zero exit code
            )

            if operation and operation.upper() == "OPTIMIZE":

                speciesId = insertSpecies(f'{job_id} opt', job_id, stage='output')

                extract_geometries(
                    f"tmp/{job_id}.out", f"tmp/{speciesId}.xyz")

                convert_xyz_to_sdf(
                    f"tmp/{speciesId}.xyz", f"tmp/{speciesId}.sdf")

                uploadFile(f"{speciesId}.sdf", speciesId, 'Species/', localDir='tmp/')

            uploadFile(f"{job_id}.out", job_id, "Calculation/", localDir="tmp/")
            update_job(job_id, nproc=0)
            job_done = True

        except subprocess.CalledProcessError as e:
            if not e.returncode == -2:

                update_job(job_id, "failed", nproc=0)
                uploadFile(f"{job_id}.out", job_id, "Calculation/", localDir="tmp/")

            cleanUp(job_id)
            print(f"\n Job failed with exit code {e.returncode}.")
            job_done = True
            job_failed = True


def run_job(nproc=None):
    """
    Run the job based on the specified package and number of processors.

    Args:
        nproc (int, optional): Number of processors to use. Defaults to None.

    Raises:
        SystemExit: If the job is interrupted by the user.

    Returns:
        None
    """

    global job_done
    global operation
    global job_failed
    print("Press Ctrl + C at any time to exit.")

    # Loop over to run the queue
    while True:

        id, package, operation = setUp()
        downloadFile(id)

        if package == "GAMESS US" and check_gamess_installation:
            if not nproc:

                nproc = get_cpu_core_count()

            # Create a thread to run the 'rungms' command
            rungms_thread = threading.Thread(
                target=run_rungms, args=(id, nproc))

            try:

                update_job(id, "in progress",
                          nproc if nproc else get_cpu_core_count())  # type: ignore

                print(f"Job Id: {id}")
                rungms_thread.start()  # Start the 'rungms' command thread

                while not job_done:

                    waiting_message(package)

                rungms_thread.join()  # Wait for the 'rungms' command thread to finish
                cleanUp(id)

                if not job_failed:

                    print_color("Job completed successfully.", "32")

                job_done = False
                job_failed = False

            except KeyboardInterrupt as exc:

                update_job(id, "interrupted", nproc=0)
                cleanUp(id)
                print("Job interrupted.       ")
                raise SystemExit from exc

        elif package == "NWChem" and is_nwchem_installed:

            # Create a thread to run the 'nwchem' command
            nwchem_thread = threading.Thread(
                target=run_nwchem, args=(id, nproc))

            try:

                update_job(id, "in progress",
                          nproc if nproc else get_cpu_core_count())  # type: ignore

                print(f"Job Id: {id}")
                nwchem_thread.start()  # Start the 'rungms' command thread

                while not job_done:

                    waiting_message(package)

                nwchem_thread.join()  # Wait for the 'rungms' command thread to finish
                cleanUp(id)

                if not job_failed:

                    print_color("Job completed successfully.", "32")

                job_done = False
                job_failed = False

            except KeyboardInterrupt as exc:

                update_job(id, "interrupted", nproc=0)
                cleanUp(id)
                print("Job interrupted.       ")
                raise SystemExit from exc

        else:
            print(f"No package called: {package}. Contact support.")
            raise SystemExit
