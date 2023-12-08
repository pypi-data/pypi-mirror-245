import subprocess

def pdf_totext(pdf_path, output_dir):
    """
    Convert a PDF file to markdown using the 'nougat' tool and save the result in the specified output directory.

    Parameters:
    - pdf_path (str): The path to the input PDF file.
    - output_dir (str): The directory where the generated markdown file will be saved.

    Raises:
    - subprocess.CalledProcessError: If the 'nougat' command fails to execute.

    Prints:
    - Success message if the PDF is converted and saved successfully.
    - Error message if there's a subprocess error.

    Example:
    >>> pdf_totext('path/to/input.pdf', 'output/directory')
    PDF generated successfully in the 'output/directory' directory.
    """
    command = f"nougat --markdown pdf '{pdf_path}' --out '{output_dir}'"
    
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"PDF generated successfully in the '{output_dir}' directory.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
