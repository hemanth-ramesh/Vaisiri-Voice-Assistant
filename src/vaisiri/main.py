import click
from vaisiri.ui.modern_gui import VaisiriAdvancedGUI

@click.command()
@click.option('--gui', is_flag=True, help='Launch the GUI.')
def main(gui):
    print("🚀 Starting Vaisiri Voice Assistant...")
    if gui:
        VaisiriAdvancedGUI().run()

if __name__ == '__main__':
    main()
