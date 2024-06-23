from skyfield.api import load, Topos
from datetime import timezone, datetime, timedelta


class PosisisHilal:
    def __init__(
        self,
        tahun,
        bulan,
        tanggal,
        jam_ij,
        menit_ij,
        detik_ij,
        jam_gh,
        menit_gh,
        detik_gh,
        langitude,
        longitude,
        elevetion,
        timezone_ofset,
    ):
        self.ts = load.timescale()
        self.eph = load("de421.bsp")
        self.earth, self.sun, self.moon = (
            self.eph["earth"],
            self.eph["sun"],
            self.eph["moon"],
        )
        self.observer_loc = Topos(
            latitude_degrees=langitude,
            longitude_degrees=longitude,
            elevation_m=elevetion,
        )
        timezone_offset = timedelta(hours=timezone_ofset)

        self.tahun = tahun
        self.bulan = bulan
        self.tanggal = tanggal
        self.date_time_gh = (
            datetime(tahun, bulan, tanggal, jam_gh, menit_gh, detik_gh).replace(
                tzinfo=timezone.utc
            )
            - timezone_offset
        )
        self.date_time = datetime(tahun, bulan, tanggal, jam_ij, menit_ij, detik_ij)

    def posisi_hilal(self):
        t = load.timescale().utc(self.date_time_gh)

        sun_posisi_obs = (
            (self.earth + self.observer_loc).at(t).observe(self.sun).apparent()
        )
        moon_posisi_obs = (
            (self.earth + self.observer_loc).at(t).observe(self.moon).apparent()
        )

        altitude_sun = sun_posisi_obs.altaz()[0].degrees
        altitude_moon = moon_posisi_obs.altaz()[0].degrees

        return altitude_sun, altitude_moon

    def jika_time(self):
        treshold_time = datetime(self.tahun, self.bulan, self.tanggal, hour=17)

        condition_time = self.date_time > treshold_time
        posisi_hilal = self.posisi_hilal()[1]
        posisi_hilal_matahari = self.posisi_hilal()[0] > posisi_hilal

        if condition_time:
            self.date_time += timedelta(days=1)
        elif posisi_hilal < 0:
            self.date_time += timedelta(days=1)
        else:
            self.date_time

        return self.date_time

    def get_jika_hilal(self):
        adust_date_time = self.jika_time()
        return (
            adust_date_time.year,
            adust_date_time.month,
            adust_date_time.day,
            adust_date_time.hour,
            adust_date_time.minute,
            adust_date_time.second,
        )
