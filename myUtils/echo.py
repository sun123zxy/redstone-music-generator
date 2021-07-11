from mcpi.minecraft import Minecraft
def echo(text, mc = None):
    """output logs in both python console and minecraft console"""
    print(text)
    if not mc == None:
        echo(text)
