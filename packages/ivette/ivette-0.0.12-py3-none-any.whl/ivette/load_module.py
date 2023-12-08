"""Module for handling input/output operations."""

import itertools
import logging

from .IO_module import (
    create_charge_multiplicity_array,
    create_string_array,
    file_exists,
    get_valid_input,
    verify_file_extension,
    exists,
    cleanUp
)

from .file_io_module import (
    generate_nwchem_input_from_sdf,
    convert_xyz_to_sdf,
    get_files_with_extension,
    get_word_at_position,
    nwchem_to_xyz,
    replace_start_directive
)

from .supabase_module import (
    insertSpecies,
    uploadFile,
    insert_job,
    update_job
)

logging.getLogger("httpx").setLevel(logging.CRITICAL)

# Available packages:
available_packages = ['NWChem']


def load_job(filename: str):
    """
    Load a job from a file.

    Args:
        filename (str): The name of the file.

    Raises:
        SystemExit: If the file does not exist or the package is not supported.
    """
    if file_exists(filename, "./"):
        
        if verify_file_extension(filename, ['.sdf']):

            print("The file is recognized as a .sdf")
            print("An .nw input file will be created.")

            # Argument input
            name = input('Enter the job name: ')
            description = input('Enter a description: ')
            package = available_packages[get_valid_input(
                f"Software available:\n1 - {available_packages[0]}\nSelect a package: ", 1, 2) - 1]

            if package == available_packages[0]:

                # Validation implementation required
                basis = input("Enter a valid basis set: ")
                functional = input("Enter a valid functional: ")
                charge = int(input("Enter the system charge: "))
                multiplicity = int(input("Enter the system multiplicity: "))
                operation = input("Operation: ")
                # Add maxiter, maxcycle, etc.

                charge = int(charge)  # Convert charge from string to int
                multiplicity = int(multiplicity)  # Convert multiplicity from string to int

                job_id = insert_job(name, package, operation, description)  # Define job_id variable
                print("Job id:", job_id)

                generate_nwchem_input_from_sdf(
                    filename,
                    basis,
                    charge,
                    job_id,
                    functional=functional,
                    multiplicity=multiplicity,
                    operation=operation
                )
                print(f"Loading job: {filename.replace('.sdf', '.nw')}")

                speciesId = insertSpecies(filename, job_id)
                if speciesId is None:
                    raise ValueError("Failed to insert species")

                update_job(job_id, 'pending')

                uploadFile(filename.replace('.sdf', '.nw'), job_id, 'Job/')
                uploadFile(filename, speciesId, 'Species/')

                print("Job loaded successfully")

            else:
                print("Currently, we don't have support for the selected package.")
                raise SystemExit

        elif verify_file_extension(filename, ['.nw']):
            # Argument input
            name = input('Enter the job name: ')
            description = input('Enter a description: ')
            package = available_packages[0]
            print("Loading job:", filename)
            operation = get_word_at_position(filename, 'task', 2)
            job_id = insert_job(name, package, operation, description)

            print("Job id:", job_id)
            replace_start_directive(filename, job_id)
            nwchem_to_xyz(filename, f"{job_id}.xyz")
            convert_xyz_to_sdf(f"{job_id}.xyz", f"{job_id}.sdf")

            uploadFile(filename, job_id, 'Job/')
            uploadFile(f"{job_id}.sdf", job_id, 'Species/')

            insertSpecies(f"{job_id}.sdf", job_id)
            update_job(job_id, 'pending')

            cleanUp(job_id)
            print("Job loaded successfully")

        else:

            print("The file extension is not supported.")
            raise SystemExit
        
    else:
        
        print(f"The file {filename} does not exist.")
        raise SystemExit


def load_project(directory: str, extension='.sdf'):
    """
    Load a project from a directory.

    Args:
        directory (str): The directory path.
        extension (str, optional): The file extension to filter. Defaults to '.sdf'.

    Raises:
        SystemExit: If the directory does not exist or the package is not supported.
    """
    if not directory.endswith('/'):
        directory += '/'

    if exists(directory):
        name = input('Enter the project name: ')
        description = input('Enter the project description: ')
        packages = create_string_array("Enter the packages (q to quit): ")

        for package in packages:
            if not check_packages([package], available_packages):
                print(
                    f"Currently, we don't have support for the {package} package.")
                raise SystemExit

        files = get_files_with_extension(directory, extension)
        print("Files with extension", extension,
              "in directory", directory, ":", files)
        basis_sets = create_string_array("Enter basis sets (q to quit): ")
        functionals = create_string_array("Enter functionals (q to quit): ")
        # Warning the multiplicity is sytem dependent, modify it
        charge_multiplicities = create_charge_multiplicity_array(
            "Enter charge and then multiplicity (q to quit): ")
        operations = create_string_array(
            "Enter operations in the order required (q to quit): ")
        
        required_Job = None

        for package in packages:
            if package == available_packages[0]:
                for basis, functional, charge_multiplicity in itertools.product(basis_sets, functionals, charge_multiplicities):
                    for file in files:
                        for operation in operations:
                            charge, multiplicity = charge_multiplicity
                            PATH = directory + file
                            
                            job_id = insert_job(
                                name,
                                package,
                                operation,
                                description,
                                charge=charge,
                                multiplicity=multiplicity,
                                functional=functional,
                                basisSet=basis,
                                requiredJobId=required_Job # type: ignore
                            )
                            print("Job id:", job_id)

                            generate_nwchem_input_from_sdf(
                                PATH,
                                basis,
                                charge,
                                job_id,
                                functional=functional,
                                multiplicity=multiplicity,
                                operation=operation
                            )
                            print(f"Loading job: {PATH.replace('.sdf', '.nw')}")

                            speciesId = insertSpecies(PATH, job_id)
                            update_job(job_id, 'pending')

                            uploadFile(PATH.replace('.sdf', '.nw'), job_id, 'Job/')
                            uploadFile(PATH, speciesId, 'Species/')

                            required_Job = job_id
                            print("Job loaded successfully")
                        
                        required_Job = None

    else:
        print(f"The directory {directory} does not exist.")
        raise SystemExit


def check_packages(packages: list, available_packages: list) -> bool:
    """
    Check if a list of packages is supported.

    Args:
        packages (list): The list of packages to check.
        available_packages (list): The list of available packages.

    Returns:
        bool: True if all packages are supported, False otherwise.
    """
    return all(package in available_packages for package in packages)
