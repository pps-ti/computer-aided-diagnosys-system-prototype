# :computer: Purwarupa Sistem Diagnosis Penyakit Daring

<p align="justify">
&emsp;&emsp;Neuratest merupakan <i>platform</i> daring yang dapat digunakan untuk mendeteksi (klasifikasi) beberapa penyakit berdasarkan anatomi citra kesehatan.</p>

<p align="center">
  <img src="https://neuratest.site/static/img/logo.jpg">
</p>

<p align="justify">
&emsp;&emsp;<i>Platform</i> ini menggunakan Flask sebagai <i>Backend Framework</i> yang ditulis dalam bahasa pemrograman Python, serta Firebase sebagai <i>database</i> dan <i>storage</i>. Hanya ada dua tipe <i>user</i> dalam program ini, yaitu Admin dan Wakil dari sebuah rumah sakit. Fitur untuk kedua tipe pengguna tersebut akan dijelaskan lebih lanjut. Berikut ini adalah ilustrasi hubungan antar <i>tools</i> yang digunakan dalam membangun Neuratest :
</p>

<p align="center">
  <img src="https://i.imgur.com/7FXP70e.jpg">
</p>

Keterangan tiap tools :<br>
1. <i>Frontend</i> kami menggunakan <a href="https://getbootstrap.com/">Bootstrap</a> yang beberapa .css dan .js nya ada yang kami buat/kustom sendiri.<br>
2. Layanan email kami menggunakan <a href="https://pythonhosted.org/Flask-Mail/">Flask Mail</a> yang langsung terintegrasi dengan Google Mail.<br>
3. Kami menggunakan <a href="https://palletsprojects.com/p/flask/">Flask</a> sebagai framework utama.<br>
4. Untuk mengakses <i>realtime database</i> dan <i>cloud storage</i> yang berada pada Firebase server kami menggunakan <a href="https://github.com/nhorvath/Pyrebase4">Pyrebase4</a>.<br>
6. Website ini dihosting pada layanan yang memanfaatkan <a href="https://github.com/phusion/passenger">Phusion Passenger</a> sebagai server <i>deployment</i>'nya Flask.<br><br>

## :memo: Panduan memulai
Silahkan ketik perintah berikut ini secara berurutan pada terminal(Linux/Mac) atau CMD(Windows) kalian jika ingin mencoba untuk menjalankannya pada <i>localhost</i> masing-masing :
### 1 <i>pull</i> atau <i>clone</i> repositori ini

```
$ git clone https://github.com/pps-ti/computer-aided-diagnosys-system-prototype.git
$ cd computer-aided-diagnosys-system-prototype
```
atau
```
$ mkdir computer-aided-diagnosys-system-prototype
$ cd computer-aided-diagnosys-system-prototype
$ git init
$ git pull https://github.com/pps-ti/computer-aided-diagnosys-system-prototype.git
```

### 2 Instal <i>libraries</i>/<i>frameworks</i>'nya
```
pip3 install -r requirements.txt
```
atau
```
pip install -r requirements.txt
```

### 3 Jalankan di <i>localhost</i>
```
python3 main.py
```
atau
```
python main.py
```

### 4 Akses http://127.0.0.1:5000/
<i>Landing page</i> FIK-OCW :<br><br>
![permalink setting demo](https://i.ibb.co/0hsgpcC/Screenshot-from-2020-12-13-18-18-04.png)
Ketik <b>ctrl + c</b> pada terminal/CMD kalian jika ingin mematikan server flask'nya.<br>
<p align="justify">
<b><i>DISCLAIMER</i></b> : Karena memperhatikan faktor keamanan pada <i>cloud storage/database</i>, kami tidak mencantumkan <i>API keys</i> dari Firebase serta akun yang digunakan untuk menggunakan flask mail. Jadi merupakan hal yang wajar apabila jika menjalankan program ini secara <i>default</i> setelah kalian melakukan <i>pull</i>/<i>clone</i> repositori ini akan terjadi kegagalan. Hubungi saja pengelola repositori ini jika benar-benar ingin memahami struktur <i>database</i> dan <i>storage</i>'nya
<p>

## :handshake: Kontribusi
Silahkan <i>fork</i> repositori ini terlebih dahulu setelah itu kalian bebas mengembangkan proyek ini.

## :paperclip: Lisensi
<a href="https://github.com/Rakhid16/fp-pemframework/blob/master/LICENSE">Creative Commons Zero v1.0 Universal</a>

## :sunglasses: Fitur Aplikasi
<b>1. Pengunjung Umum</b>
- [x] <i>Landing Page</i>
- [x] <i>Login</i>
- [x] Mendaftar

<b>2. Admin</b>
- [x] Ubah sandi akun
- [x] Lihat data wakil rumah sakit yang aktif maupun belum
- [x] Hapus data wakil rumah sakit yang aktif maupun belum
- [x] Edit data wakil rumah sakit yang aktif maupun belum
- [x] Tambah akun baru untuk wakil rumah sakit
- [x] Keluar <i>dashboard</i>

<b>3. Perwakilan Rumah Sakit</b>
- [x] Edit data diri dan mengatur ulang sandi yang terlupa
- [x] Melakukan diagnosa dari beberapa penyakit yang tersedia melalui citra
- [x] Melaporkan isu yang ditemukan oleh pengguna
- [x] Melihat hasil diagnosa
- [x] Mengubah data dari pasien yang telah terdiagnosa
- [x] Menghapus data pasien
- [x] Keluar <i>dashboard</i>

## :movie: Dokumentasi
<a href="https://www.youtube.com/watch?v=106l8evECYg&t=260s"><i>Python Conference Asia Pacific 2020</i></a>