import uvicorn
import click

from app.server import server
from utils.etc import get_mods
from utils.config import Config

welcome_text = """
   _____                      _                 _    
  / ____|                    | |               | |   
 | (___  _ __   __ _  ___ ___| |__   ___   ___ | | __
  \___ \| '_ \ / _` |/ __/ _ \ '_ \ / _ \ / _ \| |/ /
  ____) | |_) | (_| | (_|  __/ |_) | (_) | (_) |   < 
 |_____/| .__/ \__,_|\___\___|_.__/ \___/ \___/|_|\_\ 
        | |                                          
        |_| 작품의 가치를 더하세요.
"""

command_help = f"""
{welcome_text}\n

Spacebook Backend

Usage: python(x) run.py [mode]

available mods: {get_mods()}
(edit on config.yml)
"""


@click.command(help=command_help)
@click.argument("mode")
def cli_command(mode: str):
    print(welcome_text + "\n")
    print("Spacebook Backend (fastapi, tortoise-orm)\n")
    print(f"Runtime Option | [mode]: {mode}")
    config = Config("config.yml", mode=mode)
    server.config = config
    uvicorn.run(
        server, host=config.get("host", "0.0.0.0"), port=config.get("port", 8000)
    )


if __name__ == "__main__":
    cli_command()
