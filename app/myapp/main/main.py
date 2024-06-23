from .pilih import Pilih
from ..core.ijtima import DataIjtimak
from ..core.jamghurub import Jamghurub
from ..core.conversidate import Konversi
from ..core.skyfield_data import DataCalculator
from ..core.posisi_hilal import PosisisHilal
from ..core.namahari_bulan import TanggalIndonesia
from rich.console import Console
from rich.table import Table


class TampilData:
    def __init__(self):
        self.jamghurub = Jamghurub()
        self.konversi = Konversi()
        self.dataastro = DataCalculator()
        self.console = Console()
        self.ijtimak = DataIjtimak()
        self.nama = TanggalIndonesia()

    def pilih_main(
        self, nama_tempat: str, bulan: str, tahun: int, before: int, after: int
    ):
        try:
            pilih = Pilih()
            select_data = pilih.pilih_tempat(nama_tempat)

            _, nama_tempat, latitude, longitude, elevetion, timezone = select_data

            def konversi_bulan(nama_bulan: str):
                try:
                    bulan_hijri = {
                        "Muhharam": 1,
                        "Safar": 2,
                        "Rabiul Awal": 3,
                        "Rabiul Akhir": 4,
                        "Jumadil Ula": 5,
                        "Jumadil Akhir": 6,
                        "Rajab": 7,
                        "Syaban": 8,
                        "Ramadhan": 9,
                        "Syawal": 10,
                        "Zulkaidah": 11,
                        "Zulhijah": 12,
                    }
                    konversiBulan = bulan_hijri.get(nama_bulan.strip(), None)
                    return int(konversiBulan) if konversiBulan is not None else None
                except KeyError:
                    handle = self.console.print(
                        "[yellow] Input Bulan Hjriah Salah Gunakan Nama-nama Bulan Hinjriah Sebagai berikut: Muhharam, Safar, Rabiul Awal, Rabiul, Akhir, Jumadil Awal, Jumadil Ula, Rajab, Syaban, Ramadhan, Syawal, Zulkaidah, Zulhijah[/yellow]"
                    )
                    return handle

            hasil_konversi = konversi_bulan(bulan)
            bulan_hijriah = int(hasil_konversi)

            tahun_hijrih = tahun

            masehi_konversi = self.konversi.hijri_to_masehi(tahun_hijrih, bulan_hijriah)
            (
                tanggal_masehi,
                namabulan_masehi,
                bulan_masehi,
                tahun_masehi,
            ) = masehi_konversi
            (
                tahun_ij,
                bulan_ij,
                tanggal_ij,
                jam_ij,
                menit_ij,
                detik_ij,
            ) = self.ijtimak.conjungsi(tahun_masehi, bulan_masehi, tanggal_masehi)

            (
                tahun_gh,
                bulan_gh,
                tanggal_gh,
                jam_gh,
                menit_gh,
                detik_gh,
            ) = self.jamghurub.get_sunset_time_ephem(
                latitude, longitude, elevetion, timezone, tahun_ij, bulan_ij, tanggal_ij
            )

            adjuster = PosisisHilal(
                tahun_gh,
                bulan_gh,
                tanggal_gh,
                jam_ij,
                menit_ij,
                detik_ij,
                jam_gh,
                menit_gh,
                detik_gh,
                latitude,
                longitude,
                elevetion,
                timezone,
            )
            tahun_pre, bulan_pre, tanggal_pre, _, _, _ = adjuster.get_jika_hilal()

            hari_ij, namabulan_ij = self.nama.tentukan_hari(
                tahun_ij, bulan_ij, tanggal_ij
            )
            hari_pre, namabulan_pre = self.nama.tentukan_hari(
                tahun_pre, bulan_pre, tanggal_pre
            )

            data_astro = {
                "year": tahun_pre,
                "month": bulan_pre,
                "day": tanggal_pre,
                "hours": jam_gh,
                "minute": menit_gh,
                "timezone_offset": timezone,
                "langitude": latitude,
                "longitude": longitude,
                "elevetion": elevetion,
                "beforeTime": before,
                "afterTime": after,
            }
            dataAsto_hilal = self.dataastro.generate_data(data_astro)
            self.console.print(
                f"[yellow]Data Astronomi Hilal Untuk {nama_tempat}[/yellow]",
                justify="center",
            )
            self.console.print(
                f"[green] Koordinat: {round(latitude, 4)} LS {round(longitude,4)} BT {elevetion} meter {timezone} GMT[/green]",
                justify="center",
            )

            self.console.print(
                f"[yellow] Ijtimak Terjadi Pada Hari {hari_ij} {tanggal_ij} {namabulan_ij} {tahun_ij} pada jam {jam_ij}:{menit_ij}:{detik_ij}[/yellow]",
                justify="center",
            )
            self.console.print(
                f"[yellow]Akhir Bulan Terjadi Pada Hari {hari_pre} {tanggal_pre} {namabulan_pre} {tahun_pre}[/yellow]",
                justify="center",
            )
            self.console.print(
                f"[green]Dan Terbenam Matahari Terjadi Pada Jam {jam_gh}:{menit_gh}[/green]",
                justify="center",
            )

            table = Table(
                title=f"Data Astronomi Untuk Akhir Bulan {bulan} {tahun_hijrih}",
                show_header=True,
                header_style="bold yellow",
            )
            for column in dataAsto_hilal.columns:
                table.add_column(column)

            for index, row in dataAsto_hilal.iterrows():
                table.add_row(*[str(value) for value in row])
            self.console.print(table, justify="center")
        except Exception as e:
            console = Console()
            console.print(
                "[red]!!! Terjadi Kesalahan Perhatikan Penulisan Command line nya !!!  [/red]"
            )
