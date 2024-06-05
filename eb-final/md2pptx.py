import pypandoc
import tempfile
import os

def clean_markdown_content(markdown_text):
    """ Clean the markdown content by removing any text before the first h1 header """
    lines = markdown_text.split('\n')
    clean_lines = []
    found_h1 = False
    for line in lines:
        if line.startswith("# "):
            found_h1 = True
        if found_h1:
            clean_lines.append(line)
    return '\n'.join(clean_lines)

def convert_markdown_to_pptx(markdown_text, output_file='output.pptx', template=None):
    # Ensure Pandoc is available
    try:
        pypandoc.get_pandoc_version()
    except OSError:
        pypandoc.download_pandoc()

    
    # clean the markdown content
    markdown_text = clean_markdown_content(markdown_text)
    
    # Create a temporary markdown file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.md') as temp_md_file:
        temp_md_file.write(markdown_text.encode('utf-8'))
        temp_md_filename = temp_md_file.name

    try:
        # Define the extra arguments for pypandoc
        extra_args = [] 
        if template:
            extra_args.extend(['--reference-doc', template])

        # Convert the markdown file to pptx using pypandoc
        pypandoc.convert_file(temp_md_filename, 'pptx', outputfile=output_file, extra_args=extra_args)
    finally:
        # Remove the temporary markdown file
        os.remove(temp_md_filename)

    return output_file