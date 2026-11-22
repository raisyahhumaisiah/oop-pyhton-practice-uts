class Buku:
    __total_buku = 0

    def __init__(self, kode, judul, penulis, stok):
        self.__kode = Buku.validasi_teks(kode, "Kode buku").upper()
        self.judul = judul
        self.penulis = penulis
        self.stok = stok
        Buku.__total_buku += 1

    @property
    def kode(self):
        return self.__kode

    @property
    def judul(self):
        return self.__judul

    @judul.setter
    def judul(self, nilai):
        self.__judul = Buku.validasi_teks(nilai, "Judul")

    @property
    def penulis(self):
        return self.__penulis

    @penulis.setter
    def penulis(self, nilai):
        self.__penulis = Buku.validasi_teks(nilai, "Penulis")

    @property
    def stok(self):
        return self.__stok

    @stok.setter
    def stok(self, nilai):
        if not isinstance(nilai, int) or nilai < 0:
            raise ValueError("Stok harus bilangan bulat >= 0.")
        self.__stok = nilai

    def perkenalan(self):
        print(f"[BUKU] {self.kode} | {self.judul} | {self.penulis} | Stok: {self.stok}")

    def respons(self, aksi):
        if aksi == "pinjam":
            if self.stok == 0:
                return f"Maaf, buku '{self.judul}' sedang habis."
            self.stok -= 1
            return f"Buku '{self.judul}' berhasil dipinjam. Sisa stok: {self.stok}"
        if aksi == "kembali":
            self.stok += 1
            return f"Buku '{self.judul}' dikembalikan. Stok sekarang: {self.stok}"
        return "Aksi tidak dikenal (gunakan 'pinjam' atau 'kembali')."

    @classmethod
    def total_buku(cls):
        return cls.__total_buku

    @classmethod
    def dari_string(cls, teks):
        bagian = [b.strip() for b in teks.split(";")]
        if len(bagian) != 4 or not bagian[3].isdigit():
            raise ValueError("Format harus: kode;judul;penulis;stok (stok angka).")
        return cls(bagian[0], bagian[1], bagian[2], int(bagian[3]))

    @staticmethod
    def validasi_teks(nilai, nama_field):
        if not isinstance(nilai, str) or not nilai.strip():
            raise ValueError(f"{nama_field} tidak boleh kosong.")
        return nilai.strip()


class Anggota:

    BATAS_PINJAM = 3  

    def __init__(self, id_anggota, nama):
        self.__id_anggota = Anggota.validasi_id(id_anggota)
        self.nama = nama
        self.__daftar_pinjam = []  

    @property
    def id_anggota(self):
        return self.__id_anggota

    @property
    def nama(self):
        return self.__nama

    @nama.setter
    def nama(self, nilai):
        if not isinstance(nilai, str) or len(nilai.strip()) < 3:
            raise ValueError("Nama minimal 3 karakter.")
        self.__nama = nilai.strip().title()

    @property
    def daftar_pinjam(self):
        return list(self.__daftar_pinjam)

    def perkenalan(self):
        print(f"[ANGGOTA] Halo, saya {self.nama} (ID: {self.id_anggota}). "
              f"Sedang meminjam {len(self.__daftar_pinjam)} buku.")

    def respons(self, pesan):
        pesan = pesan.lower()
        if "halo" in pesan:
            return f"Halo juga, {self.nama}! Mau pinjam buku apa hari ini?"
        if "pinjaman" in pesan:
            if not self.__daftar_pinjam:
                return "Kamu belum meminjam buku apa pun."
            return "Buku yang kamu pinjam: " + ", ".join(self.__daftar_pinjam)
        return "Maaf, saya belum paham pesanmu."

    def pinjam_buku(self, buku):
        if len(self.__daftar_pinjam) >= Anggota.BATAS_PINJAM:
            return f"{self.nama} sudah mencapai batas {Anggota.BATAS_PINJAM} buku."
        if buku.judul in self.__daftar_pinjam:
            return f"{self.nama} sudah meminjam '{buku.judul}'."
        hasil = buku.respons("pinjam")
        if hasil.startswith("Buku") and "berhasil" in hasil:
            self.__daftar_pinjam.append(buku.judul)
        return hasil

    def kembalikan_buku(self, buku):
        if buku.judul not in self.__daftar_pinjam:
            return f"{self.nama} tidak sedang meminjam '{buku.judul}'."
        self.__daftar_pinjam.remove(buku.judul)
        return buku.respons("kembali")

    @classmethod
    def anggota_baru(cls, nama):
        nama_bersih = Buku.validasi_teks(nama, "Nama")
        return cls("AG-" + nama_bersih[:3].upper(), nama_bersih)

    @staticmethod
    def validasi_id(id_anggota):
        if not isinstance(id_anggota, str) or not id_anggota.startswith("AG-"):
            raise ValueError("ID anggota harus diawali 'AG-'.")
        return id_anggota


class Perpustakaan:
    def __init__(self, nama):
        self.nama = nama
        self.__buku = {}     
        self.__anggota = {}   

    @property
    def nama(self):
        return self.__nama

    @nama.setter
    def nama(self, nilai):
        self.__nama = Buku.validasi_teks(nilai, "Nama perpustakaan")

    def perkenalan(self):
        print(f"=== Selamat datang di {self.nama} ===")
        print(f"Koleksi: {len(self.__buku)} judul | Anggota: {len(self.__anggota)} orang")

    def respons(self, perintah):
        if perintah == "daftar":
            return "\n".join(
                f"- {b.kode}: {b.judul} (stok {b.stok})" for b in self.__buku.values()
            ) or "Belum ada buku."
        return "Perintah tidak dikenal."

    def tambah_buku(self, buku):
        if buku.kode in self.__buku:
            raise ValueError(f"Kode {buku.kode} sudah terdaftar.")
        self.__buku[buku.kode] = buku

    def daftar_anggota(self, anggota):
        self.__anggota[anggota.id_anggota] = anggota

    def cari_buku(self, kode):
        return self.__buku.get(kode.upper())


if __name__ == "__main__":
    perpus = Perpustakaan("Perpustakaan Kampus")

    b1 = Buku("B001", "Pemrograman Python", "Salwa Salsa.F", 2)
    b2 = Buku("B002", "Struktur Data", "Keisya R.F", 1)
    b3 = Buku.dari_string("B003; Basis Data ; Murinah ; 3")
    for b in (b1, b2, b3):
        perpus.tambah_buku(b)

    a1 = Anggota("AG-001", "Devina Sri.M")
    a2 = Anggota.anggota_baru("Erin")
    perpus.daftar_anggota(a1)
    perpus.daftar_anggota(a2)

    
    perpus.perkenalan()
    print()
    b1.perkenalan()
    a1.perkenalan()
    print()

    
    print(a1.respons("Halo"))
    print(a1.pinjam_buku(b1))
    print(a1.pinjam_buku(b2))
    print(a2.pinjam_buku(b2))
    print(a1.respons("pinjaman saya"))
    print(a1.kembalikan_buku(b1))
    print()
    print("Daftar buku:")
    print(perpus.respons("daftar"))
    print(f"\nTotal objek Buku dibuat: {Buku.total_buku()}")

    
    print("\n--- Uji validasi ---")
    try:
        Buku("B004", "", "Penulis", 1)
    except ValueError as e:
        print("Error:", e)
    try:
        b1.stok = -5
    except ValueError as e:
        print("Error:", e)
    try:
        Anggota("123", "Budi")
    except ValueError as e:
        print("Error:", e)
