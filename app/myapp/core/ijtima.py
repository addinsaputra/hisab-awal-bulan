from skyfield import almanac
from skyfield.api import load
import os
from datetime import datetime, timedelta


class DataIjtimak:
    def __init__(self):
        self.ts = load.timescale()
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        eph_path = os.path.join(base_dir, 'de440.bsp')
        self.eph = load(eph_path)
        self.earth, self.sun, self.moon = (
            self.eph["earth"],
            self.eph["sun"],
            self.eph["moon"],
        )

    def conjungsi(self, year, month, day):
        date = datetime(year, month, day)
        t1 = self.ts.utc(date.year, date.month, date.day)
        t2 = t1 + timedelta(days=2)

        f = almanac.oppositions_conjunctions(self.eph, self.moon)
        t, _ = almanac.find_discrete(t1, t2, f)

        t_utc_iso = t.utc_iso()[0]

        y = int(t_utc_iso[0:4])
        mo = int(t_utc_iso[5:7])
        d = int(t_utc_iso[8:10])
        ho = int(t_utc_iso[11:13])
        mi = int(t_utc_iso[14:16])
        s = int(t_utc_iso[17:19])

        return y, mo, d, ho, mi, s


if __name__ == "__main__":
    print("ijtima.py: ready")
