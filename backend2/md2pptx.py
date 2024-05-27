# md2pptx.py
import subprocess
import tempfile
import os

def convert_markdown_to_pptx(markdown_text, output_file='output.pptx', template='template.pptx'):
    # Create a temporary markdown file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.md') as temp_md_file:
        temp_md_file.write(markdown_text.encode('utf-8'))
        temp_md_filename = temp_md_file.name

    try:
        # Define the command to run pandoc
        pandoc_command = [
            'pandoc',
            temp_md_filename,
            '-o', output_file,
            '--from', 'markdown',
            '--to', 'pptx'
        ]

        # Include the template if provided
        if template:
            pandoc_command.extend(['--reference-doc', template])

        # Run the pandoc command
        subprocess.run(pandoc_command, check=True)
    except FileNotFoundError as e:
        print("Pandoc is not installed or not found in your PATH. Please install Pandoc and ensure it is available in your PATH.")
        raise e
    finally:
        # Remove the temporary markdown file
        os.remove(temp_md_filename)

    return output_file