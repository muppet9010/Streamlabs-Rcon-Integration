# https://github.com/uncaught-exceptions/mcrcon
from mcrcon import MCRcon
with MCRcon('mikeserver', 'TesT') as mcr:
    resp = mcr.command(
        '/sc rcon.print("players: " .. #game.connected_players)')
    mcr.command('/sc game.print("test")')
    print(resp)
