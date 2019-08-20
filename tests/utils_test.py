import unittest

from server.utils import *


def test_time_conversion():
    t  = datetime(2013,12,1,1,5,7)
    unix_time = datetime_to_unix(t)

    c_t = unix_to_datetime(unix_time)
    print(c_t)
    assert (t== c_t)