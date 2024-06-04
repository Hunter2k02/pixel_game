import pygame

pygame.init()
# Colors
LIGHTBLUE = (72, 128, 247)
AZURE = (240, 255, 255)
DARK_GREY = (169, 169, 169)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (34, 177, 76)
PINK = (255, 174, 201)
PANTONE = (98, 100, 102)
CRIMSON = (220, 20, 60)

WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

ENEMIES_RESPAWN_TIME = 5000
FPS = 60

TILESIZE = 64
TEXT_LAYER = 4
PLAYER_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 20


# MAP  150x100xTILESIZE px

tilemap = """
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
B..............TTT.................................................................................B
B..............TTT........................e........................................................B
B..............TTT.......................e.e...........a.........a.........TTTTTTTTTTTT............B
B..............TTT.....................................ea..D..............TTTDTTTTTTTTTTTTT....a...B
B..............TTT............TTTTTTTTTTTT............TTTTTT.............TTT.....TTTTT.TTTTT...as..B
B..............TTT..........TTTTTTTTTTTTTTTD........TTTTTTTTTT....TTTTTTTTT..............TTTT......B
B..............TTTD......TTTTTTTTTTTTTTTTTTTT...TTTTTTT.....TTTTTTTTTTTTTT....a...........TTTT.....B
B..............TTT.....TTTTT..............TTTTTTTTTTT.......TTTTTT.........................TTTT....B
B..............TTTT...TTTT.................TTTTTT...........TTT.........a..........a.......DTTT....B
B...............TTTTTTTT.....................TTTD...........TTT........aa....a.............TTTT....B
B................TTTTTT.......e...............e.............TTT.................s.........TTTT.....B
B.................TTT........e.e..............ea............TTT..........................TTTT..s...B
B.................TTT.......................................TTTTTTTTT..................TTTTT.......B
B.....e...........TTT......................OOOOOOO...........TTTTTTTTTTTT........TTTTTTTTTTT.......B
B....e.e.........TTT..................OOOOOOWWWWWWOOOOOOOO.........TTTTTTT.....TTTDTTTTTTTTT.......B
B...............TTTTD..OOOOOOOOOOOOOOOOWWWWWWWWWWWWWWWWWWOOOOOOO........TTT...TTT.....aa.TTT.......B
B..............TTTT..OOOWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWOOOO......TTTTTTT.....sa...TTT......B
B..............TTTT.OOOWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWOOOOOO..TTTT...........TTT......B
B.............TTTT.OWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWO..TTTOOOOOOOOOOOTTTOOOOOOB
B............TTTT..OWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWOODTTTOOOOOOOOOOOOTTTOOOOOB
B...........TTTT....OOWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWTTTWWWWWB
B...........TTT......OOWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWOOOTTTOOOOOOOOOOOOTTTOOOOOB
B...........TTT......OOWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWO...TTTTD........TTTT.....B
B...........TTT....OOWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWO...TTT.........TTTT.......B
B...........TTT.....OOWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWOO...TTT.....TTTTTTT.........B
B.......a..TTTTD.......OOOWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWOOOOOOOO...TTTTTTTTTTTTT..........B
B.......aeTTTT...........OOOOOOWWWWWWWWWWWWWWWWWWWWWWWWWWWWOOOOOOO......TTTTTTTTTTTTT..............B
B.........TTTT.................OOOOOOOOOOOWWWWWWWWWWWWWOOOOO....TTTTTTTTTTTTTTD....................B
B.........TTTD...........................OOOOOOOOOOOOOO......TTTTTTTTTTTTTTT.......................B
B.........TTTT...........es...............................TTTTTTD..................................B
B..........TTTT..........a...........s..................TTTTT............................ss........B
B...........TTTT.....................ss...............TTTD.TT............................as........B
B...........DTTT......................................TTTTTT.......................................B
B............TTT...................................DTTTTTTTT......ss...............................B
B...aa........TTT..............TTT................TTTT...TTT.......a.........ss....................B
B...a..........TTTTD.........TTTTTTT.......s...TTTTTTT...TTT.................a.....................B
B...............TTTTT......TTTTTTTTTTD......s..TTTT.......TTT......................................B
B................TTTTTTTTTTTT.....TTTTTTT....s.TTTD........TTTT....................................B
B...................TTTTTTTD.........TTTTTTTTTTT.....s..s....TTTT..................................B
B.......................................TTTTTTTT...ss.b.s.....TTTTT................................B
B.........ea................................DTTTD...s..s.........TTTT..............................B
B..........s.................................TTTT..................TTTT..............ss............B
B............................................TTTT....................TTT.............ss............B
B......................................s......TTTT....................TTT..........................B
B......................................ssd....TTTT.....................TTT.........................B
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBTTTTBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBTTTTBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB..................................................B
B..............................r........TTTTTTTTTT..R..............................................B..................................................B
B...............TTTT..................TTTTTTTTTTTT.s....R....................r.........r...........B..................................................B
B...R.....w...TTTTTTT.........R.....TTTTT.s...TTTT.....r....................w......................B..................................................B
B........b.w.TTTT..TTTT...r........TTTTT....R.TTTT..................r.........b....................B..................................................B
B.....R.....TTTT...TTTT..........TTTTT...r....TTTT......R....................w..R..................B..................................................B
B..........TTTT.....TTTT..w.b.TTTTTT......bb..TTTT..........................................R......B..................................................B
B..........TTTT......TTTT.b...TTTT..s...b.....TTTT.................................................B..................................................B
B.....w...TTTT.......TTTTTTTTTTTT.....R.....TTTTTT.R...............R...................R...........B..................................................B
B.....bw...TTTT....s..TTTTTTTTTTTT..........TTTTTTTT........r.........................R............B..................................................B
B....r.....TTTT.R..s.TTTT...rTTTTTT........TTTTTTTTTT.....................R........................B..................................................B
B..........TTTT...s..TTTT........TTTTT.....TTTTT.TTTTT...............w.............................B..................................................B
B...........TTTT.s..TTTT..R..s....TTTTT..TTTTTT...TTTTT............w..b............................B..................................................B
B............TTTT..TTTT............TTTTTTTTTTT.....TTTTTT..........................................B..................................................B
B.............TTTTTTTT....s.R.......TTTTTTTTT..R....TTTTTTTT............s..........................B..................................................B
B.................TTT..............rTTTTT............TTTTTTTT.....R................................B..................................................B
B.................TTT..........s....TTTTT...r...s...TTTTTTTTTT..................R..................B..................................................B
B.........r.....s.TTT..s.............TTTT...........TTTT..TTTT.....................................B..................................................B
B.................TTT....R...r........TTTT.R.......TTTT...TTTTT.........RRRRRRRRRRRRRRRRRRRRRRRRRRRB..................................................B
B.................TTTT..................TTTT......TTTT.....wTTTT........RRRRRRRRRRRRRRRRRRRRRRRRRRRB..................................................B
B..............R...TTTT....r...R.........TTTT....TTTT.....w.w.TTTT......RRRRRR...s.................B..................................................B
B....................TTTT.....s...........TTTTTTRTTT...........TTTTT....RRRRRR..s.......s...s......B..................................................B
B...............s.....TTTT..s.........R....TTTTTTTT............TTTTT....RRRRR...s....s.......s.....B..................................................B
B....................s.TTTTT..............TTTT...................TTTTuuuuRRRR.....s....s.s.s..s....B..................................................B
B...................s..TTTTTTT...........TTTT............u........TTTTTuuuRRR...s...s..s.s.s.s......S.................................................B
B.............u..R...sTTTTTTTTT........TTTT.............uuu........TTTTTuuRRR...s..s.s.s.s....s.s...S.................................................B
B............uu..s.s.TTTTuuuuTTTT......TTTT...........uuuuuu.R....u..TTTTuuRR.s..s.s.s.s.s..s......B..................................................B
Buu....R...uuuuuR..TTTTTuuuuuTTTTTTTTTTTT....Ru......uuuuuHuu....uuu.TTTTTRRR...s...s...s...s.s..s.B..................................................B
Buuuu....uuuuuuuuTTTTTTuuuHuuuuTTTTTTTTT....uuuu...uuuuuuuuuuuu.uuuuuuTTTTTRR...s..s.s...s.s.s.....B..................................................B
BuuHuuuuuuuuuuuuTTTTuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuHuuuuuuuuuuuuuuuuuuuuuRRRRRRRRRRRRRR...RRRRRRRB..................................................B
BuuuuuuuHuuuuuHuTTTTuuuHuuuuuuuHuuuuuuuHuuuuuHuuuuuHuuHuuuuuuHuuuHuuuuuuHuuuuuuRRRRRRRRRRRs..RRRRRRB..................................................B
BuuuHuuuuuuuuuuuTTTTuuuuuHuuuuuuuHuuuuuuuuuuuuuuuuuuuuuuuHuuuuuuuuuuHuuuuuuuuuRRRRRRRRRRR...RRRRRRRB..................................................B
Buuuu...uuu.....TTT..uuuuuuHuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuHuuuuuuuuuuuu...........s.........B..................................................B
Buu......u....TTTTT......uuuuu.......TTTTTuuu....uuuuuuuHuuHuuuuuuu.......TTTT.........s.s.........B..................................................B
B............TTTTT.........uu.........TTTTT..........uuuuuuuuuuuu..........TTTTT.......s...........B..................................................B
B...........TTTTT...........u..........TTTTT............uuuuuuu..............TTTTT..s....s.R.......B..................................................B
B............TTTTT.....................TTTTT..............uuu.................TTTTT..s.............B..................................................B
B........R.....TTTTT...................TTTTT.......R.......u.............R....TTTTT................B..................................................B
B...............TTTTT............R......TTTTT..................................TTTTT...............B..................................................B
B................TTTTT...................TTTTT..................................TTTTT..........R...B..................................................B
B.................TTTTT....................TTTTT....................R............TTTTT.............B..................................................B
B............R.....TTTTTT..........R.........TTTTT................................TTTTT............B..................................................B
B...R................TTTTT....................TTTTT...............................TTTTTT...........B..................................................B
B.....................TTTTT...................TTTTT................TTTTTT.......TTTTTTTTT..........B..................................................B
B.................R....TTTTTTTTTTTTTT..........TTTTTTTTTT.....TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT.......B..................................................B
B.......................TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT......B..................................................B
B.......R................TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT......TTTTTTT.......TTTTTTT.....B..................................................B
B....................................TTTTTTTTTTTTTTT.....TTTTT............................TTTTTTT..B..................................................B
B........................R...........................................R.....................TTTTTTTTB..................................................B
B...........................................................................................TTTTTTTB..................................................B
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
"""
tilemap = tilemap.split()
