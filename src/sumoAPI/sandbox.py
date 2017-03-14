import trafcodLink, re

theString = "light <0> <rrrrr>"
splitString = re.split('<|>', theString)


tcConnect = trafcodLink.trafcodLink('localhost',10000)

tcConnect.handshakeTrafcod()

tcConnect.sendDetectorToTrafcod("0", 1)

tcConnect.askTrafcodToAdvance()

tcConnect.recieveTrafcodLightStates()


