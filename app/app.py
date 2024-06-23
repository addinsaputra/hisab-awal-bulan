import typer
import shutil
from myapp.view import viewcreat
from myapp.crud import Delete, read
from myapp.crud import select
from myapp.view import updatedata
from myapp.main import main, print


def ceter_text(text: str) -> str:
    terminal_width = shutil.get_terminal_size().columns
    text_width = len(text)
    left_padding = (terminal_width - text_width) // 2
    centered_lines = " " * left_padding + text
    return centered_lines


app = typer.Typer(
    help=ceter_text(
        "Aplikasi Hilal Tracker\n\n"
        "Aplikasi ini diperuntukan untuk mendapatkan Data Hilal Permenit\n\n"
        "Daftar Nama Bulan Hijriah:\n\n - Muhharam \n\n - Safar \n\n - Rabiul Awal \n\n - Rabiul Akhir \n\n - Jumadil Ul        a \n\n - Jumadil Akhir \n\n - Rajab \n\n - Syaban \n\n - Ramadhan \n\n - Syawal \n\n - Zulkaidah \n\n - Zulhijah         \n\n !!! PERINGATAN !!! \n\n Perhartikan setiap hurufnya dan command yang digunakan"
    )
)


@app.command()
def cloc():
    """
    Untuk Membuat Dan Menambahkan Data Tempat Baru Ke Database
    Gunakan Comand: python app/app.py cloc
    """
    view_tambah = viewcreat.ViewCreat()
    view_tambah.tambah_data()


@app.command()
def vloc():
    """
    Untuk Menampilkan Seluruh Data Tempat Yang Tersimpan
    Gunakan Comand: python app/app.py vloc
    """
    lihat_data = read.Read()
    lihat_data.lihat_tempat()


@app.command()
def sch(nama: str):
    """
    Untuk Mencari Data Tempat
    Gunakan Comand: python app/app.py sch "nama tempat"
    """
    select_data = select.Select()
    select_data.pilih_tempat(nama)


@app.command()
def ul(nama_tempat: str):
    """
    Untuk Memperbaharui Data Tempat
    Gunakan Comand: python app/app.py ul "nama tempat"
    """
    perbaharui_data = updatedata.UpdateData()
    perbaharui_data.update_data(nama_tempat)


@app.command()
def delt(nama_tempat: str):
    """
    Untuk Menghapus Data Tempat
    Gunakan Comand: python app/app.py del "nama tempat"
    """
    hapus_data = Delete()
    hapus_data.hapus_tempat(nama_tempat)


@app.command()
def view(
    nama: str,
    bulan: str,
    tahun: int,
    before: int = typer.Option(
        None, "-b", help="Sebelum berapa menit terbenam matahari(e.g., -b 30)"
    ),
    after: int = typer.Option(
        None, "-a", help="Sesudah berapa menit terbenam matahari(e.g., -a 31)"
    ),
):
    """
    Untuk Melihat Data Astronomi Hilal
    Gunakan Comand: python app/app.py view "nama tempat" "bulan hijriah" tahun hijriah -b (sebelum berapa menit) -a sesudah berapa menit)
    """
    pilihan = main.TampilData()
    pilihan.pilih_main(nama, bulan, tahun, before, after)


@app.command()
def svap(
    nama: str,
    bulan: str,
    tahun: int,
    before: int = typer.Option(
        None, "-b", help="Sebelum berapa menit terbenam matahari(e.g., -b 30)"
    ),
    after: int = typer.Option(
        None, "-a", help="Sesudah berapa menit terbenam matahari(e.g., -a 31)"
    ),
):
    """
    Untuk Mencetak Data Astronomi Hilal ke Bentuk PDF
    Gunakan Comand: python app/app.py svap "nama tempat" "bulan hijriah" tahun hijriah -b (sebelum berapa menit) -a sesudah berapa menit)
    """

    cetak = print.PrintData()
    cetak.print_main(nama, bulan, tahun, before, after)


if __name__ == "__main__":
    app()
