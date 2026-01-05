from skyfield.api import load, Topos, Angle
import os
from skyfield import almanac
from datetime import timedelta, timezone, datetime
import pandas as pd


class DataCalculator:
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

        self.data = {
            "Jam": [],
            "Altitude Sun": [],
            "Azimut Sun": [],
            "Altitude Moon": [],
            "Azimut Moon": [],
            "Elongasi": [],
            "Ilumination": [],
        }

    def generate_data(self, data):
        year = data["year"]
        month = data["month"]
        day = data["day"]
        hours = data["hours"]
        minute = data["minute"]
        timezone_offset = timedelta(hours=data["timezone_offset"])
        beforeTime = int(data["beforeTime"])
        afterTime = int(data["afterTime"])
        langitude = float(data["langitude"])
        longitude = float(data["longitude"])
        elevetion = float(data["elevetion"])
        start_time = (
            datetime(year, month, day, hours, minute).replace(tzinfo=timezone.utc)
            - timezone_offset
        )

        before_time = start_time - timedelta(minutes=beforeTime)
        after_time = start_time + timedelta(minutes=afterTime)
        current_time = before_time

        while current_time <= after_time:
            t = load.timescale().utc(
                current_time.year,
                current_time.month,
                current_time.day,
                current_time.hour,
                current_time.minute,
                current_time.second,
            )
            observer_loc = Topos(
                latitude_degrees=langitude,
                longitude_degrees=longitude,
                elevation_m=elevetion,
            )

            sun_posisi_obs = (
                (self.earth + observer_loc).at(t).observe(self.sun).apparent()
            )
            moon_posisi_obs = (
                (self.earth + observer_loc).at(t).observe(self.moon).apparent()
            )
            time = current_time + timezone_offset
            # ketinggian & azimut sun
            altitude_sun = sun_posisi_obs.altaz()[0].degrees
            azimut_sun = sun_posisi_obs.altaz()[1].degrees

            # ketinggian moon
            altitude_moon = moon_posisi_obs.altaz()[0].degrees
            azimut_moon = moon_posisi_obs.altaz()[1].degrees

            # elongasi bulan
            elongasi = sun_posisi_obs.separation_from(moon_posisi_obs)
            degree_el, menit_el, second_el = Angle.dms(elongasi)

            # ilumination bulan
            ilumination = almanac.fraction_illuminated(self.eph, "moon", t) * 100

            def format_dms(degrees):
                sign = -1 if degrees < 0 else 1
                decimal_degrees = abs(degrees)
                degrees = int(decimal_degrees) * sign
                minutes = int((decimal_degrees - abs(degrees)) * 60)
                seconds = (decimal_degrees - abs(degrees) - minutes / 60) * 3600

                return f"{degrees}° {minutes}' {seconds:.2f}\""

            # masukan data
            self.data["Jam"].append(f"{time.strftime('%H:%M')}")
            self.data["Altitude Sun"].append(f"{format_dms(altitude_sun)}")
            self.data["Azimut Sun"].append(f"{format_dms(azimut_sun)}")
            self.data["Altitude Moon"].append(f"{format_dms(altitude_moon)}")
            self.data["Azimut Moon"].append(f"{format_dms(azimut_moon)}")
            self.data["Elongasi"].append(
                f"{round(degree_el)}° {round(menit_el)}' {second_el:.2f}\""
            )
            self.data["Ilumination"].append(f"{round(ilumination, 3)}%")

            current_time += timedelta(minutes=1)

        return pd.DataFrame(self.data)


if __name__ == "__main__":
    print("skyfield_data.py: ready")
