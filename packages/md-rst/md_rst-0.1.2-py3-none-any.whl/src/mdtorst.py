import os
import click
import pypandoc

def install_pandoc():
    """ 
    Try install Pandoc with 
    pypandoc.download_pandoc()
    """
    click.echo("Pandoc is not installed. Installing Pandoc...")
    try:
        pypandoc.download_pandoc()
    except Exception as e:
        click.echo(f"Error installing Pandoc: {e}")
        raise click.Abort()

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path(), required=False)
def convert_md_to_rst(input_file, output_file):
    """
    Convert a Markdown file to reStructuredText.

    \b
    --> INPUT_FILE: Input Markdown file name
    <-- OUTPUT_FILE: Output reStructuredText file name (Optional)
    """
    # Get current directory
    user_directory = os.getcwd()

    # If output_file is not provided, construct the output file name
    if not output_file:
        base_name, _ = os.path.splitext(os.path.basename(input_file))
        output_file = os.path.join(user_directory, f"{base_name}.rst")
    else:
        output_file = os.path.join(user_directory, output_file)

    try:
        # Try to convert the Markdown file to reStructuredText
        output = pypandoc.convert_file(input_file, 'rst', format='markdown')

        # Save the result to the specified output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)

        click.echo(f"Successful conversion: {input_file} -> {output_file}")
    except Exception as e:
        # If there is an error, try to install Pandoc and then retry the conversion
        click.echo(f"Error during conversion: {e}")
        install_pandoc()
        try:
            output = pypandoc.convert_file(input_file, 'rst', format='markdown')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            click.echo(f"Successful conversion after installing Pandoc: {input_file} -> {output_file}")
        except Exception as e:
            click.echo(f"Error after installing Pandoc: {e}")
            raise click.Abort()
