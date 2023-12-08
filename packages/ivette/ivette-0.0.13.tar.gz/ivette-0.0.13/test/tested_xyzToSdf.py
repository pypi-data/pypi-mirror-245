from openbabel import pybel


def convert_xyz_to_sdf(input_file, output_file):
    """
    Convert a NWChem input file to a .sdf file using Open Babel.

    Parameters:
    - input_file (str): Path to the input NWChem file.
    - output_file (str): Path to the output .sdf file.
    """
    # Create an Open Babel molecule object
    mol_generator = pybel.readfile("xyz", input_file)
    mol = next(mol_generator)

    # Output the molecule to a .sdf file
    with open(output_file, 'w') as sdf_file:
        sdf_file.write(mol.write("sdf"))


# Example usage:
if __name__ == "__main__":
    nw_file_path = "public/output.xyz"
    sdf_file_path = "output.sdf"
    convert_xyz_to_sdf(nw_file_path, sdf_file_path)
