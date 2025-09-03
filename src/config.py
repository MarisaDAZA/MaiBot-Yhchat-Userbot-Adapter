import tomlkit

with open('config.toml', 'r', encoding='utf-8') as f:
    config = tomlkit.load(f)