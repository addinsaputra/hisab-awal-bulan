from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .pilih import Pilih
from ..core.jamghurub import Jamghurub
from ..core.conversidate import Konversi
from ..core.skyfield_data import DataCalculator
from ..core.ijtima import DataIjtimak
from ..core.posisi_hilal import PosisisHilal
from ..core.namahari_bulan import TanggalIndonesia
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from rich.console import Console
from rich.prompt import Prompt
import os


class PrintData:
    def __init__(self):
        self.jamghurub = Jamghurub()
        self.konversi = Konversi()
        self.dataastro = DataCalculator()
        self.console = Console()
        self.ijtimak = DataIjtimak()
        self.nama = TanggalIndonesia()

    def print_main(
        self, nama_tempat: str, bulan: str, tahun: int, before: int, after: int
    ):
        try:
            pilih = Pilih()
            select_data = pilih.pilih_tempat(nama_tempat)

            _, nama_tempat, latitude, longitude, elevetion, timezone = select_data

            def konversi_bulan(nama_bulan: str):
                bulan_hijri = {
                    "Muharram": 1,
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

            filename = Prompt.ask("Masukan Nama File PDF : ", default="output")
            directory = Prompt.ask(
                "Tentukan Folder/Direktori Yang Dinginkan :", default="./"
            )

            if not os.path.exists(directory):
                self.console.print(
                    "[bold red] ALERT :[/bold red] Folder/Direktory Tidak Ditemukan atau Belum Ada !!!"
                )
                exit()

            file_path = os.path.join(directory, filename + ".pdf")

            pdf = SimpleDocTemplate(file_path, pagesize=letter)

            table_data = [
                dataAsto_hilal.columns.tolist()
            ] + dataAsto_hilal.values.tolist()
            table = Table(table_data)

            style = TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.green),
                    ("TEXTCOLOR", (0, 0), (-1, 0), (1, 1, 1)),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("GRID", (0, 0), (-1, -1), 1, (0, 0, 0)),
                ]
            )
            for i in range(1, len(dataAsto_hilal)):
                bg_color = colors.lightgreen if i % 2 == 0 else colors.whitesmoke

                style.add("BACKGROUND", (0, i), (-1, i), bg_color)

            table.setStyle(style)

            title_style = ParagraphStyle(
                name="Title", fontName="Times-Bold", fontSize=14, alignment=1
            )
            title = Paragraph(
                f"<b> Data Astronomi Hilal {nama_tempat} Untuk Hari {hari_pre} {tanggal_pre} {namabulan_pre} {tahun_pre}</b>",
                title_style,
            )
            deskripsi_text2 = f" Ijtimak Terjadi pada Hari {hari_ij} {tanggal_ij} {namabulan_ij} {tahun_ij} jam {jam_ij}:{menit_ij}"
            deskripsi_style2 = ParagraphStyle(
                name="Explanation", fontName="Times-Roman", fontSize=12, alignment=1
            )
            deskripsi2 = Paragraph(deskripsi_text2, deskripsi_style2)

            deskripsi_text = f"Koordinat : {round(latitude, 4)} Derajat LS {round(longitude, 4)} Derajat BT {elevetion} meter {timezone}-GMT"
            deskripsi_style = ParagraphStyle(
                name="Explanation", fontName="Times-Roman", fontSize=12, alignment=1
            )
            deskripsi = Paragraph(deskripsi_text, deskripsi_style)
            spacer = Spacer(1, 16)
            spacer2 = Spacer(1, 6)
            spaser3 = Spacer(1, 16)
            tulisan = [title, spaser3, deskripsi2, spacer2, deskripsi, spacer, table]

            pdf.build(tulisan)

            self.console.print(
                f"Data Telah di cetak dalam bentuk PDF dengan Nama File [bold cyan]{filename}.pdf[/bold cyan] di Folder/Direktory [bold cyan]{directory}[/bold cyan]."
            )
        except Exception as e:
            console = Console()
            console.print(
                f"[red]!!! Terjadi Kesalahan Silakan Periksa penulisan Comand line !!! Error: {e}[/red]"
            )
