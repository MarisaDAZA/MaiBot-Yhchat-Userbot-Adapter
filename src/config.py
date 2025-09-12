import tomlkit

with open('config.toml', 'r', encoding='utf-8') as f:
    config = tomlkit.load(f)

config.group_list = [str(i) for i in config.group_list]
config.private_list = [str(i) for i in config.private_list]
config.ban_user_id = [str(i) for i in config.ban_user_id]
