from datetime import datetime

class TanggalIndonesia:
    # Kamus nama hari dalam bahasa Indonesia
    nama_hari_indonesia = {
        "Monday": "Senin",
        "Tuesday": "Selasa",
        "Wednesday": "Rabu",
        "Thursday": "Kamis",
        "Friday": "Jumat",
        "Saturday": "Sabtu",
        "Sunday": "Minggu"
    }

    # Kamus nama bulan dalam bahasa Indonesia
    nama_bulan_indonesia = {
        1: "Januari",
        2: "Februari",
        3: "Maret",
        4: "April",
        5: "Mei",
        6: "Juni",
        7: "Juli",
        8: "Agustus",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "Desember"
    }

    @classmethod
    def tentukan_hari(cls, tahun, bulan, hari):
               # Membuat objek datetime dari input tanggal
        input_date = datetime(tahun, bulan, hari)

        # Mendapatkan nama hari dari tanggal yang dimasukkan
        nama_hari = input_date.strftime("%A")
        nama_hari_indonesia_res = cls.nama_hari_indonesia.get(nama_hari, "Unknown")

        # Mendapatkan nama bulan dari tanggal yang dimasukkan
        nama_bulan = input_date.month
        nama_bulan_indonesia_res = cls.nama_bulan_indonesia.get(nama_bulan, "Unknown")

        # Format tanggal dalam bahasa Indonesia

        return nama_hari_indonesia_res, nama_bulan_indonesia_res

