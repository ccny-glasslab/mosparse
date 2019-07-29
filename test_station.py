from dateutil.tz import tzutc 
import datetime
import mav_parse as mp
import pandas as pd

def test_get_header():
    header = mp.get_header(' KMVY   GFS MOS GUIDANCE    1/04/2019  1800 UTC                      \n')
    truth = {'station':'KMVY', 'short_model':'GFS', 'model':'GFS MOS GUIDANCE', 'runtime':datetime.datetime(2019,1,4,18,0, tzinfo=tzutc())}
    assert header==truth
    
def test_get_fntime():
    row1 = ' DT /JAN   2                  /JAN   3                /JAN   4       \n'
    row2 = ' HR   00 03 06 09 12 15 18 21 00 03 06 09 12 15 18 21 00 03 06 12 18 \n'
    fntimes = mp.get_fntime(row1,row2,{'station':'KSTS', 'model':'GFS MOS GUIDANCE', 'runtime':datetime.datetime(2019,1,1,18,0, tzinfo=tzutc())}) 
    truth = [datetime.datetime(2019, 1, 2, 0, 0), datetime.datetime(2019, 1, 2, 3, 0), datetime.datetime(2019, 1, 2, 6, 0), datetime.datetime(2019, 1, 2, 9, 0), datetime.datetime(2019, 1, 2, 12, 0), datetime.datetime(2019, 1, 2, 15, 0), datetime.datetime(2019, 1, 2, 18, 0), datetime.datetime(2019, 1, 2, 21, 0), datetime.datetime(2019, 1, 3, 0, 0), datetime.datetime(2019, 1, 3, 3, 0), datetime.datetime(2019, 1, 3, 6, 0), datetime.datetime(2019, 1, 3, 9, 0), datetime.datetime(2019, 1, 3, 12, 0), datetime.datetime(2019, 1, 3, 15, 0), datetime.datetime(2019, 1, 3, 18, 0), datetime.datetime(2019, 1, 3, 21, 0), datetime.datetime(2019, 1, 4, 0, 0), datetime.datetime(2019, 1, 4, 3, 0), datetime.datetime(2019, 1, 4, 6, 0), datetime.datetime(2019, 1, 4, 12, 0), datetime.datetime(2019, 1, 4, 18, 0)]
    assert fntimes==truth
    
def test_get_fntime_date_values():
    row1 = ' DT /JULY 15            /JULY 16                /JULY 17          /  \n'
    row2 = ' HR   06 09 12 15 18 21 00 03 06 09 12 15 18 21 00 03 06 09 12 18 00 \n'
    fntimes = mp.get_fntime(row1,row2,{'station':'K0V1', 'model':'AVN MOS GUIDANCE', 'runtime':datetime.datetime(2000,7,15,0,0, tzinfo=tzutc())}) 
    truth = [datetime.datetime(2000, 7, 15, 6, 0), datetime.datetime(2000, 7, 15, 9, 0), datetime.datetime(2000, 7, 15, 12, 0), datetime.datetime(2000, 7, 15, 15, 0), datetime.datetime(2000, 7, 15, 18, 0), datetime.datetime(2000, 7, 15, 21, 0), datetime.datetime(2000, 7, 16, 0, 0), datetime.datetime(2000, 7, 16, 3, 0), datetime.datetime(2000, 7, 16, 6, 0), datetime.datetime(2000, 7, 16, 9, 0), datetime.datetime(2000, 7, 16, 12, 0), datetime.datetime(2000, 7, 16, 15, 0), datetime.datetime(2000, 7, 16, 18, 0), datetime.datetime(2000, 7, 16, 21, 0), datetime.datetime(2000, 7, 17, 0, 0), datetime.datetime(2000, 7, 17, 3, 0), datetime.datetime(2000, 7, 17, 6, 0), datetime.datetime(2000, 7, 17, 9, 0), datetime.datetime(2000, 7, 17, 12, 0), datetime.datetime(2000, 7, 17, 18, 0), datetime.datetime(2000, 7, 18, 0, 0)]
    assert fntimes==truth

def test_get_fntimes_june():
    row1 = ' DT /MAY 31 /JUNE01 /JUNE02'
    row2 = ' HR   00 12 00 12 00 12    '
    truth = [datetime.datetime(2000, 5, 31, 0, 0), datetime.datetime(2000, 5, 31, 12, 0), datetime.datetime(2000, 6, 1, 0, 0), datetime.datetime(2000, 6, 1, 12, 0), datetime.datetime(2000, 6, 2, 0, 0), datetime.datetime(2000, 6, 2, 12, 0)]
    fntimes =  mp.get_fntime(row1,row2,{'station':'K0V1', 'model':'AVN MOS GUIDANCE', 'runtime':datetime.datetime(2000,5,30,18,0, tzinfo=tzutc())}) 
    assert truth==fntimes

def test_get_fntime_yearend():
    row1 = ' DT /DEC   31/JAN   1    /   \n'
    row2 = 'HR   06 12 18 00 06 12 18 00 \n'
    
    fntimes = mp.get_fntime(row1,row2,{'station':'KNYC', 'model':'GFS MOS GUIDANCE', 'runtime':datetime.datetime(2000,12,31,0,0, tzinfo=tzutc())})
    truth = [datetime.datetime(2000,12,31,6,0), datetime.datetime(2000,12,31,12,0), datetime.datetime(2000,12,31,18,0), datetime.datetime(2001,1,1,0,0), datetime.datetime(2001,1,1,6,0), datetime.datetime(2001,1,1,12,0), datetime.datetime(2001,1,1,18,0), datetime.datetime(2001,1,2,0,0)]
    
    assert fntimes==truth
    
def test_get_fntime_leap_year():
    row1 = ' DT /FEB  27      /FEB  28                /FEB  29             /     \n'
    row2 = ' HR   12 15 18 21 00 03 06 09 12 15 18 21 00 03 06 09 12 15 18 00 06 \n'
    fntimes = mp.get_fntime(row1, row2,{'station':'KNYC', 'model':'GFS MOS GUIDANCE', 'runtime':datetime.datetime(2016,2,27,6,0, tzinfo=tzutc())})
    
    truth = [datetime.datetime(2016, 2, 27, 12, 0), datetime.datetime(2016, 2, 27, 15, 0), datetime.datetime(2016, 2, 27, 18, 0), datetime.datetime(2016, 2, 27, 21, 0), datetime.datetime(2016, 2, 28, 0, 0), datetime.datetime(2016, 2, 28, 3, 0), datetime.datetime(2016, 2, 28, 6, 0), datetime.datetime(2016, 2, 28, 9, 0), datetime.datetime(2016, 2, 28, 12, 0), datetime.datetime(2016, 2, 28, 15, 0), datetime.datetime(2016, 2, 28, 18, 0), datetime.datetime(2016, 2, 28, 21, 0), datetime.datetime(2016, 2, 29, 0, 0), datetime.datetime(2016, 2, 29, 3, 0), datetime.datetime(2016, 2, 29, 6, 0), datetime.datetime(2016, 2, 29, 9, 0), datetime.datetime(2016, 2, 29, 12, 0), datetime.datetime(2016, 2, 29, 15, 0), datetime.datetime(2016, 2, 29, 18, 0), datetime.datetime(2016, 3, 1, 0, 0), datetime.datetime(2016, 3, 1, 6, 0)]
    
    assert fntimes==truth   
def test_parse_row_all_values():
    row5 = ' DPT  14 24 29 29 28 28 32 31 30 35 34 33 32 32 37 36 35 35 34 33 38 \n'
    var,vals = mp.parse_row(row5)
    truth_var = 'DPT'
    truth_vals = ['14', '24', '29', '29', '28', '28', '32', '31', '30', '35', '34', '33', '32', '32', '37', '36', '35', '35', '34', '33', '38']
    assert var==truth_var
    assert vals==truth_vals

def test_parse_row_6():
    row3 =  ' P06         0     0     0     0     0     0     1     0     0  0  2 \n'
    var,vals = mp.parse_row(row3)
    truth_var = 'P06'
    truth_vals = [None, None, '0', None, '0', None, '0', None, '0', None, '0', None, '0', None, '1', None, '0', None, '0', '0', '2']
    assert var==truth_var
    assert vals==truth_vals
    
def test_parse_row_12():
    row3 =  ' N/X              28          57          32          55       34    \n'
    var,vals = mp.parse_row(row3)
    truth_var = 'N/X'
    truth_vals = [None, None, None, None, '28', None, None, None, '57', None, None, None, '32', None, None, None, '55', None, None, '34', None]
    assert var==truth_var
    assert vals==truth_vals
    
def test_parse_row_6p():
    row13 =  ' T06      0/ 0  0/ 4  0/ 0  0/ 0  0/ 0  0/ 1  0/ 0  0/ 0  0/ 0  0/ 0 \n'
    var,vals = mp.parse_row(row13)
    truth_var = 'T06'
    truth_vals = [None, None, '0/ 0', None, '0/ 4', None, '0/ 0', None, '0/ 0', None, '0/ 0', None, '0/ 1', None, '0/ 0', None, '0/ 0', None, '0/ 0', None, '0/ 0']
    assert var==truth_var
    assert vals==truth_vals
    

def test_parse_row_12p():
    row13 =  ' T12                  0/ 9        0/ 0        0/ 4        0/ 0  0/ 3 \n'
    var,vals = mp.parse_row(row13)
    truth_var = 'T12'
    truth_vals = [None, None, None, None, None, None, '0/ 9', None, None, None, '0/ 0', None, None, None, '0/ 4', None, None, None, '0/ 0', None, '0/ 3']
    assert var==truth_var
    assert vals==truth_vals

def test_parse_station_empty():
    station = []
    truth = mp.parse_station(station)
    expected = pd.DataFrame()
    assert pd.DataFrame.equals(truth, expected)
    
def test_parse_station():
    station = [' KDSM   GFS MOS GUIDANCE    1/01/2019  1800 UTC                      \n', ' DT /JAN   2                  /JAN   3                /JAN   4       \n', ' HR   00 03 06 09 12 15 18 21 00 03 06 09 12 15 18 21 00 03 06 12 18 \n', ' N/X              11          32          22          40       29    \n', ' TMP  17 16 15 15 15 17 27 31 28 27 26 25 26 28 35 39 36 34 33 32 44 \n', ' DPT   7  7  7  7  6  7 11 13 14 15 16 17 18 20 23 24 25 25 25 25 29 \n', ' CLD  BK BK OV OV CL CL CL CL CL CL CL CL CL CL FW SC FW CL CL CL FW \n', ' WDR  34 27 25 23 22 22 23 24 25 27 27 26 24 21 24 23 21 22 24 24 27 \n', ' WSP  04 03 05 06 08 10 12 14 09 08 06 05 03 07 08 09 06 07 06 05 08 \n', ' P06         0     0     2     0     1     0     0     0     2  1  2 \n', ' P12               3           2           1           0        2    \n', ' Q06         0     0     0     0     0     0     0     0     0  0  0 \n', ' Q12               0           0           0           0        0    \n', ' T06      0/ 0  0/ 0  0/ 0  0/ 0  0/ 0  0/ 0  0/ 0  0/ 0  0/ 0  0/ 0 \n', ' T12                  0/ 4        1/ 1        0/ 3        0/ 0  0/ 4 \n', ' POZ   1  0  0  0  0  1  1  0  0  2  3  2  3  7  7  5  6 10  8  8  2 \n', ' POS  97100100100100 99 99100100 98 97 98 95 88 70 51 50 53 54 47 49 \n', ' TYP   S  S  S  S  S  S  S  S  S  S  S  S  S  S  S  S  S  S  S  S  S \n', ' SNW                                       0                    0    \n', ' CIG   8  8  7  7  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8 \n', ' VIS   7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7 \n', ' OBV   N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N  N \n']
    result = mp.parse_station(station)
    result.to_csv("dsm_test.csv")
    t = open("dsm_test.csv", "r")
    e = open("kdsm_x.csv", "r")
    truth = t.readlines()
    expected = e.readlines()
    for i in range(len(truth)):
        assert truth[i]==expected[i]
    

#@pytest.mark.skip()
def test_get_rows():
    header = None
    station = [' KSTS   GFS MOS GUIDANCE    1/01/2019  1800 UTC                      \n',
 ' DT /JAN   2                  /JAN   3                /JAN   4       \n',
 ' HR   00 03 06 09 12 15 18 21 00 03 06 09 12 15 18 21 00 03 06 12 18 \n',
 ' N/X              28          57          32          55       34    \n',
 ' TMP  60 48 38 34 31 32 43 54 55 43 38 36 35 34 41 52 53 45 40 36 44 \n',
 ' DPT  14 24 29 29 28 28 32 31 30 35 34 33 32 32 37 36 35 35 34 33 38 \n',
 ' CLD  FW CL CL CL FW SC FW CL FW SC CL SC BK BK SC SC BK BK BK OV OV \n',
 ' WDR  08 31 31 00 33 09 00 00 14 15 14 00 32 35 02 00 16 15 17 32 16 \n',
 ' WSP  05 03 01 00 01 01 00 00 02 03 02 00 01 01 01 00 04 03 01 01 01 \n',
 ' P06         0     0     0     0     0     0     1     0     0  0  2 \n',
 ' P12               0           1           0           2        1    \n',
 ' Q06         0     0     0     0     0     0     0     0     0  0  0 \n',
 ' Q12               0           0           0           0        0    \n',
 ' T06      0/ 0  0/ 4  0/ 0  0/ 0  0/ 0  0/ 1  0/ 0  0/ 0  0/ 0  0/ 0 \n',
 ' T12                  0/ 9        0/ 0        0/ 4        0/ 0  0/ 3 \n',
 ' POZ   1  1  3  2  1  2  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 \n',
 ' POS  18 21  8 19 25 12  0  2  0  0  0  0  0  0  0  0  0  0  0  0  0 \n',
 ' TYP   R  R  R  R  R  R  R  R  R  R  R  R  R  R  R  R  R  R  R  R  R \n',
 ' CIG   8  8  8  8  2  1  8  8  8  8  8  1  1  1  2  8  8  8  8  1  1 \n',
 ' VIS   7  7  7  7  7  1  1  6  7  7  3  2  2  1  1  6  7  5  3  1  1 \n',
 ' OBV   N  N  N  N  N FG FG HZ  N HZ BR BR FG FG FG HZ  N BR BR FG FG \n']
    return mp.get_rows(header, station)

'''def test_get_station_gz():
    truth = mp.get_stations('hello_world.txt.gz')
    expected = [['hello world, how are you'], ['1 1 2 3 5 8 13 21 34 55 89', 'lots of numbers']]
    assert truth == expected
    '''
