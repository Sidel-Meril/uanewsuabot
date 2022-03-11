# UANews bot

Bot for collecting news from official news channels and forming feed based on [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

## Description

Bot subscribes for list of channels in [official_channels.txt](official_channels.txt)
. User can edit this list after subscribing and add new channels (it not purposusaly  must be news channels)

## Getting Started

### Dependencies

[Check requirements.txt](requirements.txt)

### Installing

For starting localy you needs PostgreSQL Database and bot, registred in [BotFather](t.me/BotFather), than change _config in [sql_command.py](sql_command.py) and [bot.py](bot.py)

```
#bot.py
_config = {
    "bot":{
        "token": *YOUR TOKEN*
    }
}

#sql_command.py
_config = {
    "postgres":{
        "url": *YOUR DATABASE URL*
    }
}

```

### Executing program

[Start bot in Telegram](t.me/uanewsuabot)

## Help

test
```
test
```

