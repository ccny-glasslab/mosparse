from dateutil.tz import tzutc 
import datetime
import mav_parse as mp

def test_get_header():
    header = mp.get_header(' KMVY   GFS MOS GUIDANCE    1/04/2019  1800 UTC                      \n')
    truth = {'station':'KMVY', 'model':'GFS MOS GUIDANCE', 'runtime':datetime.datetime(2019,1,4,18,0, tzinfo=tzutc())}
    assert header==truth
def test_get_fntime():
    row1 = ' DT /JAN   2                  /JAN   3                /JAN   4       \n'
    row2 = ' HR   00 03 06 09 12 15 18 21 00 03 06 09 12 15 18 21 00 03 06 12 18 \n'
    fntimes = mp.get_fntime(row1,row2,{'station':'KSTS', 'model':'GFS MOS GUIDANCE', 'runtime':datetime.datetime(2019,1,1,18,0, tzinfo=tzutc())}) 
    truth = 