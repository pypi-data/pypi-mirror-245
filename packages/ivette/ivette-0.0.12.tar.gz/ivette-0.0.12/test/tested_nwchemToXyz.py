def nwchem_to_xyz(nw_filename, xyz_filename):
    """
    Convert NWChem input file to XYZ file.

    Parameters:
    - nw_filename (str): Path to the NWChem input file.
    - xyz_filename (str): Path to the output XYZ file.
    """
    # Read NWChem input file
    with open(nw_filename, 'r') as nw_file:
        nw_lines = nw_file.readlines()

    # Extract atomic coordinates
    atomic_coordinates = []
    start_reading_coordinates = False
    for line in nw_lines:
        if 'geometry' in line.lower():
            start_reading_coordinates = True
        elif 'end' in line.lower() and start_reading_coordinates:
            break
        elif start_reading_coordinates:
            tokens = line.split()
            if len(tokens) >= 4:
                element, x, y, z = tokens[:4]
                atomic_coordinates.append((element, float(x), float(y), float(z)))

    # Write XYZ file
    with open(xyz_filename, 'w') as xyz_file:
        xyz_file.write(f"{len(atomic_coordinates)}\n")
        xyz_file.write("Converted from NWChem input file\n")
        for atom in atomic_coordinates:
            xyz_file.write(f"{atom[0]} {atom[1]:.6f} {atom[2]:.6f} {atom[3]:.6f}\n")

# Example usage:
if __name__ == '__main__':
    nwchem_to_xyz('public/molecule.nw', 'output.xyz')
