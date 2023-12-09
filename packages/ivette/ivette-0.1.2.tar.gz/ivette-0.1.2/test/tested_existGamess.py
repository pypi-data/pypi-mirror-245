import shutil

def check_gamess_installation():
    try:
        # Check if the 'rungms' executable is in the system's PATH
        if shutil.which('rungms') is not None:
            return True
        else:
            print("GAMESS is not installed on the system.")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Example usage
check_gamess_installation()
