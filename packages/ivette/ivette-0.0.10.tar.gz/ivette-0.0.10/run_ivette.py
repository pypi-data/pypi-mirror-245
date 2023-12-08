"CLI main script for the IVETTE project."
import argparse

from ivette.load_module import load_job, load_project
from ivette.run_module import run_job
from ivette.IO_module import print_color
from ivette.supabase_module import cancel_all_jobs, downloadFile, update_job


def main():
    "Main program thread."
    parser = argparse.ArgumentParser(
        description="""Python client for Ivette Computational chemistry and
        Bioinformatics project"""
    )

    # Creating a mutually exclusive group for 'load' and 'run' flags
    group = parser.add_mutually_exclusive_group()

    group.add_argument("--load", help="Load a file", metavar="filename")
    group.add_argument("--project", help="Load a Project", metavar="directory")
    group.add_argument("--job", help="Download a job input", metavar="jobId")
    group.add_argument("--calc", help="Download a job output", metavar="jobId")
    group.add_argument(
        "--np", help="Download a calculation", metavar="nprocess")
    group.add_argument(
        "--cancel", help="Calcel a job", metavar="jobId")
    # group.add_argument("--run", help="Run the program", action="store_true")

    args = parser.parse_args()

    # Header
    print_color("-" * 40, "32")
    # 32 is the ANSI code for green, 1 makes it bold
    print_color("IVETTE CLI", "32;1")
    print_color("by Eduardo Bogado (2023) (C)", "34")  # 34 blue
    print_color("-" * 40, "34")

    # Accessing the values of the mutually exclusive flags
    if args.cancel:
        if args.cancel == "all":

            print(f"Warning: Canceling all jobs...")
            cancel_all_jobs()
            print_color("Done!", "32")

        else:

            print(f"Canceling job {args.cancel}...")
            update_job(args.cancel, "canceled")
            print_color("Done!", "32")

    elif args.load:
        load_job(args.load)
    elif args.project:
        load_project(args.project)
    elif args.job:
        print(f"Downloading job {args.job}...")
        downloadFile(args.job, "./", "Job/")
        print_color("Done!", "32")
    elif args.calc:
        print(f"Downloading calculation {args.calc}...")
        downloadFile(args.calc, "./", "Calculation/")
        print_color("Done!", "32")
    elif args.np:
        run_job(args.np)
    else:
        run_job()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as exc:
        print_color("\nIVETTE CLI exited gracefully.", "34")
        raise SystemExit from exc
