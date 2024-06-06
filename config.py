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

PLAYER_SPEED = 45


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
B....e.e.........TTT..................OOOOOOAAAAAAOOOOOOOO.........TTTTTTT.....TTTDTTTTTTTTT.......B
B...............TTTTD..OOOOOOOOOOOOOOOOAAAAAAAAAAAAAAAAAAOOOOOOO........TTT...TTT.....aa.TTT.......B
B..............TTTT..OOOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOOOO......TTTTTTT.....sa...TTT......B
B..............TTTT.OOOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOOOOOO..TTTT...........TTT......B
B.............TTTT.OAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO..TTTOOOOOOOOOOOTTTOOOOOOB
B............TTTT..OAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOODTTTOOOOOOOOOOOOTTTOOOOOB
B...........TTTT....OOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATTTAAAAAB
B...........TTT......OOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOOOTTTOOOOOOOOOOOOTTTOOOOOB
B...........TTT......OOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO...TTTTD........TTTT.....B
B...........TTT....OOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO...TTT.........TTTT.......B
B...........TTT.....OOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOO...TTT.....TTTTTTT.........B
B.......a..TTTTD.......OOOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOOOOOOOO...TTTTTTTTTTTTT..........B
B.......aeTTTT...........OOOOOOAAAAAAAAAAAAAAAAAAAAAAAAAAAAOOOOOOO......TTTTTTTTTTTTT..............B
B.........TTTT................OOOOOOOOOOOOAAAAAAAAAAAAAOOOOO....TTTTTTTTTTTTTTD....................B
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
B.....................................s......TTTT....................TTT.............ss............B
B......................................ss.....TTTT....................TTT..........................B
B........................................d....TTTT.....................TTT.........................B
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBTTTTBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBTTTTBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB..................................................B
B..............................r........TTTTTTTTTT..R..............................................B..................................................B
B......b........TTTT..................TTTTTTTTTTTT.s....R....................r.........r...........B..................................................B
B...R.....w...TTTTTTT.........R.....TTTTT.s...TTTT.....r....................w......................B..................................................B
B........b.w.TTTT..TTTT...r........TTTTT....R.TTTT.......b..........r.........b....................B..................................................B
B.....R.....TTTT...TTTT..........TTTTT...rw...TTTT......R....................w..R..................B..................................................B
B..........TTTT.....TTTT..w.b.TTTTTT.....bb...TTTT..........................................R......B..................................................B
B...b......TTTT......TTTT.b...TTTT..s.........TTTT....b.....b.................w....................B..................................................B
B.....w...TTTT..b....TTTTTTTTTTTT.....R.....TTTTTT.R...............R...................R...........B..................................................B
B.....bw...TTTT....s..TTTTTTTTTTTT..........TTTTTTTT........r.........................R............B..................................................B
B....r.....TTTT.R..s.TTTT...rTTTTTT........TTTTTTTTTT.....................R........................B..................................................B
B..........TTTT...s..TTTT........TTTTT.....TTTTT.TTTTT...............w.............................B..................................................B
B..b..w.....TTTT.s..TTTT..R..s....TTTTT..TTTTTT...TTTTT............w..W.............wWw............B..................................................B
B............TTTT..TTTT............TTTTTTTTTTT.....TTTTTT..........................................B..................................................B
B.............TTTTTTTT....s.R.......TTTTTTTTT..R....TTTTTTTT............s..........................B..................................................B
B......W..........TTT.....ww.......rTTTTT............TTTTTTTT.....R................................B..................................................B
B.................TTT......W...s....TTTTT...r...s...TTTTTTTTTT..................R..................B..................................................B
B.........r.....s.TTT..s.............TTTT...........TTTT..TTTT.....................................B..................................................B
B.................TTT....R...r........TTTT.R.......TTTT...TTTTT.........RRRRRRRRRRRRRRRRRRRRRRRRRRRB..................................................B
B......W..........TTTT..W..........W....TTTT......TTTT.....wTTTT........RRRRRRRRRRRRRRRRRRRRRRRRRRRB..................................................B
B.....W..W.....R...TTTT....r...R.........TTTT....TTTT.....w.w.TTTT......RRRRRR...s.................B..................................................B
B....................TTTT.....s...........TTTTTTRTTT...........TTTTT....RRRRRR..s.......s...s......B..................................................B
B...............sW.W..TTTT..s.........R....TTTTTTTT............TTTTT....RRRRR...s....s.......s.....B..................................................B
B..............W.M.W.s.TTTTT..............TTTT...................TTTT..LLRRRR.....s....s.s.s..s....B..................................................B
B..................s..TTTTTTT...........TTTT............L........TTTTTLLLRRR...s...s..s.s.s.s......S..................................................B
B.............L.R...sTTTTTTTTT........TTTT.............LLL........TTTTTLLRRR...s..s.s.s.s....s.s...S..................................................B
B............LL..s.s.TTTTLLLLTTTT......TTTT...........LLLLLL.R....L..TTTTRRRR.s..s.s.s.s.s..s......B.......................D..........................B
BLL....R...LLLLLR..TTTTTLLLLLTTTTTTTTTTTT....RL......LLLLLHLL....LLL.TTTTTRRR...s...s...s...s.s..s.B..................................................B
BLLLL....LLLLLLLLTTTTTTLLLHLLLLTTTTTTTTT....LLLL...LLLLLLLLLLLL.LLLLLLTTTTTRR...s..s.s...s.s.s.....B..................................................B
BLLHLLLLLLLLLLLLTTTTLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLHLLLLLLLLLLLLLLLLLLLLLRRRRRRRRRRRRRR...RRRRRRRB..................................................B
BLLLLLLLHLLLLLHLTTTTLLLHLLLLLLLHLLLLLLLHLLLLLHLLLLLHLLHLLLLLLHLLLHLLLLLLHLLLLLLRRRRRRRRRRRs..RRRRRRB..................................................B
BLLLHLLLLLLLLLLLTTTTLLLLLHLLLLLLLHLLLLLLLLLLLLLLLLLLLLLLLHLLLLLLLLLLHLLLLLLLLLRRRRRRRRRRR...RRRRRRRB..................................................B
BLLLL...LLL.....TTT..LLLLLLHLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLHLLLLLLLLLLLL...........s.........B..................................................B
BLL......L....TTTTT.i....LLLLL.......TTTTTLLL....LLLLLLLHLLHLLLLLLL...u...TTTT....f....s.s..f......B..................................................B
B............TTTTT.........LL.........TTTTT..........LLLLLLLLLLLL..........TTTTT....f..s......f....B..................................................B
B...........TTTTT...........L......u...TTTTT......u.u...LLLLLLL......f.......TTTTT..s....s.R.......B..................................................B
B......i.....TTTTT................i....TTTTT..............LLL.................TTTTT..s......f......B..................................................B
B........R.....TTTTT.i.................TTTTT.......R......uL.............R....TTTTT................B..................................................B
B......u........TTTTT..........i.R......TTTTT........................u.........TTTTT.......f.......B..................................................B
B................TTTTT.............u.....TTTTT.......................f..........TTTTT..........R...B..................................................B
B.................TTTTT......u.............TTTTT........u.......u...R............TTTTT...f.........B..................................................B
B............R.....TTTTTT..........R.........TTTTT.....u.f.....u.f....f...........TTTTT............B..................................................B
B...R................TTTTT...............u....TTTTT...............................TTTTTT...........B..................................................B
B.....................TTTTT...........u.......TTTTT................TTTTTT.......TTTTTTTTT..........B..................................................B
B........i........R....TTTTTTTTTTTTTT..........TTTTTTTTTT.....TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT.......B..................................................B
B.................u.....TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT......B..................................................B
B.......R................TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT......TTTTTTT.......TTTTTTT.....B..................................................B
B..............u......i............u.TTTTTTTTTTTTTTT.....TTTTT............................TTTTTTT..B..................................................B
B........................R.......u.................uf................R.............u.f.....TTTTTTTTB..................................................B
B...........................................................................................TTTTTTTB..................................................B
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
"""
tilemap = tilemap.split()
