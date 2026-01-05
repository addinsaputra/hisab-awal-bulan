from skyfield.api import load, Topos
import os
from skyfield import almanac
from datetime import datetime, timedelta


class Jamghurub:
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

    def get_sunset_time_ephem(
        self, latitude, longitude, altitude, timezone, tahun, bulan, tanggal
    ):
        timezone_offset = int(timezone)
        latitude_lok = float(latitude)
        longitude_lok = float(longitude)
        elevetion_lok = float(altitude)
        observer =self.earth + Topos(
            latitude=latitude_lok, longitude=longitude_lok, elevation_m=elevetion_lok
        )

        date = datetime(tahun, bulan, tanggal)
        t1 = self.ts.utc(date.year, date.month, date.day)
        t2 = t1 + timedelta(days=2)

        t, _ = almanac.find_settings(observer, self.sun, t1, t2)
        sunrise = t.utc_iso(" ")[0]

        year = int(sunrise[0:4])
        month = int(sunrise[5:7])
        day = int(sunrise[8:10])
        hour = int(sunrise[11:13]) + timezone_offset
        minute = int(sunrise[14:16])
        second = int(sunrise[17:19])
        return year, month, day, hour, minute, second


if __name__ == "__main__":
    print("jamghurub.py: ready")
