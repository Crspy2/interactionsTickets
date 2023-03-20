import os

from interactions import Client


def load(client: Client):
    handlers_dir = os.path.dirname(os.path.abspath(__file__))
    cogs_dir = os.path.join(os.path.dirname(handlers_dir), 'cogs')

    cogs = []
    for root, dirs, files in os.walk(cogs_dir):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for module in files:
            if module not in ("__init__.py", "template.py") and module[-3:] == ".py":
                module_path = os.path.join(root, module)
                module_name = module_path[len(os.path.dirname(cogs_dir)) + 1:-3].replace("/", ".")
                cogs.append(module_name)

    for cog in cogs:
        try:
            client.load_extension(cog)
        except Exception as err:
            print(f"Could not load a cog: {cog}\n{err}")
            return

    print("Loaded all commands")