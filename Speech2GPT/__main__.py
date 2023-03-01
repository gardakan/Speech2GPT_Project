"""Speech2GPT entry point."""
# Speech2GPT/__main__.py

from Speech2GPT import cli, __app_name__

def main():
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()