import click

from . import command


@click.group()
def main():
    pass


for command_name in command.__all__:
    main.add_command(getattr(command, command_name))


if __name__ == "__main__":
    main()
