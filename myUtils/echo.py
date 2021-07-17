from mcpi.minecraft import Minecraft

echo_mc = None
def echo(text):
    """output logs in both python console and minecraft console"""
    print(text)
    if not echo_mc == None:
        echo(text)
