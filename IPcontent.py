import pygeoip

gi = pygeoip.GeoIP('/opt/GeoIP/Geo.dat/')

def printRecord(tgt):
    rec = gi.record_by_name(tgt)