import argparse
import os

from . import __version__

parser = argparse.ArgumentParser()
parser.add_argument("--version", action="version", version=__version__)
# Create an argument to create a file using basic features of PyTenno
parser.add_argument("--example", action="store_true", help="Create an example file")


args = parser.parse_args()
if isinstance(args, argparse.Namespace):
    if args.example:
        location = input(
            "Please enter a directory in which to save the example file:\n  | "
        )
        path = os.path.abspath(location)
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        path = os.path.join(path, "example.py")
        with open(path, "w") as f:
            example = """
# Import asyncio to use async/await
import asyncio

# Import pytenno to use the PyTenno class
import pytenno

# Import the Platform enum to specify the default platform to scan on
from pytenno.models.enums import Platform

# Set the defaults for the client. These are not always 
# applicable (such as in this example, where everything is given anyways)
# They are also optional.
defualt_language = "en"
default_platform = Platform.pc

async def main():
    async with pytenno.PyTenno(
        default_language=defualt_language,
        default_platform=default_platform,
    ) as tenno:
        # Use the 'items' interface on the client
        # All methods are split up into the following interfaces:
        #   - auction_entries
        #   - auctions
        #   - auth
        #   - items
        #   - liches
        #   - misc
        #   - profile
        #   - rivens

        # This method returns not only the item, but also items
        # that are similar to the given item, ie. item of the same
        # set.
        items = await tenno.items.get_item("mirage prime set")
        for item in items:
            print(item.en.item_name)

asyncio.run(main())
"""
            f.write(example)
            print(f"Example file created at {path}.")
else:
    print(args)
