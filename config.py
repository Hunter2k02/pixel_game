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

PLAYER_SPEED = 4


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
B..............................r........TTTTTTTTTT..R..............................................B.s......s............s......s................s....B
B......b........TTTT..................TTTTTTTTTTTT.s....R....................r.........r...........B...s...........s.......................s..........B
B...R.....w...TTTTTTT.........R.....TTTTT.s...TTTT.....r....................w......................B.....s..s..............s.....s....................B
B........b.w.TTTT..TTTT...r........TTTTT....R.TTTT.......b..........r.........b....................B.......s..........s......................s........B
B.....R.....TTTT...TTTT..........TTTTT...rw...TTTT......R....................w..R..................B.s...s.........................s..................B
B..........TTTT.....TTTT..w.b.TTTTTT.....bb...TTTT..........................................R......B...s...............s......s.......................B
B...b......TTTT......TTTT.b...TTTT..s.........TTTT....b.....b.................w....................B...................s......s.......................B
B.....w...TTTT..b....TTTTTTTTTTTT.....R.....TTTTTT.R...............R...................R...........B.................s................................B
B.....bw...TTTT....s..TTTTTTTTTTTT..........TTTTTTTT........r.........................R............B..................................................B
B....r.....TTTT.R..s.TTTT...rTTTTTT........TTTTTTTTTT.....................R........................B..................s......s......s...s......s.....sB
B..........TTTT...s..TTTT........TTTTT.....TTTTT.TTTTT...............w.............................B..................s......s..............s......s..B
B..b..w.....TTTT.s..TTTT..R..s....TTTTT..TTTTTT...TTTTT............w..W.............wWw............B...................................s.....s...s....B
B............TTTT..TTTT............TTTTTTTTTTT.....TTTTTT..........................................B........................................s.........B
B.............TTTTTTTT....s.R.......TTTTTTTTT..R....TTTTTTTT............s..........................B............ss...s......s.....s...................B
B......W..........TTT.....ww.......rTTTTT............TTTTTTTT.....R................................B............s........s......s.....................B
B.................TTT......W...s....TTTTT...r...s...TTTTTTTTTT..................R..................B................s.....s...s.....s...s......s.....sB
B.........r.....s.TTT..s.............TTTT...........TTTT..TTTT.....................................B.....................s..................s......s..B
B.................TTT....R...r........TTTT.R.......TTTT...TTTTT.........RRRRRRRRRRRRRRRRRRRRRRRRRRRB...................................s.....s...s....B
B......W..........TTTT..W..........W....TTTT......TTTT.....wTTTT........RRRRRRRRRRRRRRRRRRRRRRRRRRRB.............s..........................s.........B
B.....W..W.....R...TTTT....r...R.........TTTT....TTTT.....w.w.TTTT......RRRRRR...s.................B.....s....s.s.....................................B
B....................TTTT.....s...........TTTTTTRTTT...........TTTTT....RRRRRR..s.......s...s......B....s..........s..................................B
B...............sW.W..TTTT..s.........R....TTTTTTTT............TTTTT....RRRRR...s....s.......s.....B...................sssss..s.......................B
B..............W.M.W.s.TTTTT..............TTTT...................TTTT..LLRRRR.....s....s.s.s..s....Bssssssssssssssssss.......s.ss.....s...s......s....B
B..................s..TTTTTTT...........TTTT............L........TTTTTLLLRRR...s...s..s.s.s.s......S.......................s.....ss...........s.......B
B.............L.R...sTTTTTTTTT........TTTT.............LLL........TTTTTLLRRR...s..s.s.s.s....s.s...S...............s....s...........s....s.....s...s..B
B............LL..s.s.TTTTLLLLTTTT......TTTT...........LLLLLL.R....L..TTTTRRRR.s..s.s.s.s.s..s......Bssssssssssssssssss.....E......s...........s.......B
BLL....R...LLLLLR..TTTTTLLLLLTTTTTTTTTTTT....RL......LLLLLHLL....LLL.TTTTTRRR...s...s...s...s.s..s.B.............................s....................B
BLLLL....LLLLLLLLTTTTTTLLLHLLLLTTTTTTTTT....LLLL...LLLLLLLLLLLL.LLLLLLTTTTTRR...s..s.s...s.s.s.....B.........s........................................B
BLLHLLLLLLLLLLLLTTTTLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLHLLLLLLLLLLLLLLLLLLLLLRRRRRRRRRRRRRR...RRRRRRRB........s...s......s.....s.........s...s..........B
BLLLLLLLHLLLLLHLTTTTLLLHLLLLLLLHLLLLLLLHLLLLLHLLLLLHLLHLLLLLLHLLLHLLLLLLHLLLLLLRRRRRRRRRRRs..RRRRRRB................s......s...................s......B
BLLLHLLLLLLLLLLLTTTTLLLLLHLLLLLLLHLLLLLLLLLLLLLLLLLLLLLLLHLLLLLLLLLLHLLLLLLLLLRRRRRRRRRRR...RRRRRRRB...........s.....s...s................s.....s.....B
BLLLL...LLL.....TTT..LLLLLLHLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLHLLLLLLLLLLLL...........s.........B........s...s......s.....s.................s......B
BLL......L....TTTTT.i....LLLLL.......TTTTTLLL....LLLLLLLHLLHLLLLLLL...u...TTTT....f....s.s..f......B................s......s..........................B
B............TTTTT.........LL.........TTTTT..........LLLLLLLLLLLL..........TTTTT....f..s......f....B...........s.....s...s...........s...s......s.....B
B...........TTTTT...........L......u...TTTTT......u.u...LLLLLLL......f.......TTTTT..s....s.R.......B................s........................s......s.B
B......i.....TTTTT.....i..........i....TTTTT..............LLL.................TTTTT..s......f......B........s...s......s.....s..........s.....s...s...B
B........R.....TTTTT.i.................TTTTT.......R......uL.............R....TTTTT................B................s......s.................s........B
B......u........TTTTT..........i.R......TTTTT........................u.........TTTTT.......f.......B...........s.....s...s............................B
B.......i........TTTTT.............u.....TTTTT.......................f..........TTTTT..........R...B................s.................................B
B.................TTTTT......u.............TTTTT........u.......u...R............TTTTT...f.........B..............s...s......s.....s..................B
B............R.....TTTTTT..........R.........TTTTT.....u.f.....u.f....f.......f...TTTTT............B......................s......s....................B
B...R.......i........TTTTT.......u.......u....TTTTT...............................TTTTTT...........B.................s.....s...s......................B
B.....................TTTTT...........u.......TTTTT........u.......TTTTTT.......TTTTTTTTT..........B......................s...........................B
B........i....u...R....TTTTTTTTTTTTTT..........TTTTTTTTTT.....TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT.......B......................s...s......s................B
B.......................TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT......B..............................s......s............B
B.......R................TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT......TTTTTTT.......TTTTTTT.....B.........................s.....s...s..............B
B....................................TTTTTTTTTTTTTTT.....TTTTT............................TTTTTTT..B..............................s...................B
B........................R...........................................R.....................TTTTTTTTB..................................................B
B...........................................................................................TTTTTTTB..................................................B
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
"""
tilemap = tilemap.split()
