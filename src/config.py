import tomlkit

with open('config.toml', 'r', encoding='utf-8') as f:
    config = tomlkit.load(f)

config['chat']['group_list'] = [str(i) for i in config['chat']['group_list']]
config['chat']['private_list'] = [str(i) for i in config['chat']['private_list']]
config['chat']['ban_user_id'] = [str(i) for i in config['chat']['ban_user_id']]
