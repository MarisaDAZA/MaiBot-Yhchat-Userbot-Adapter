import tomlkit

with open('config.toml', 'r') as f:
    config = tomlkit.load(f)