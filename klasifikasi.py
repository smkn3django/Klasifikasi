import os
import shutil
import json

def load_kategori(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['kategori']

def klasifikasikan_file(folder_tanggal, folder_tujuan, kategori_list):
    try:
        # Cek folder instansi
        instansi_path = os.path.join(folder_tanggal, 'instansi')
        if os.path.exists(instansi_path):
            print(f"Memproses folder instansi: {instansi_path}")

            # Cek semua folder NIP di dalam folder instansi
            for nip in os.listdir(instansi_path):
                nip_path = os.path.join(instansi_path, nip)

                if os.path.isdir(nip_path):  # Pastikan ini adalah folder NIP yang valid
                    print(f"Memproses NIP: {nip}")

                    # Cek semua file dalam folder NIP
                    for kategori in kategori_list:
                        file_found = False
                        for file_name in os.listdir(nip_path):
                            file_path = os.path.join(nip_path, file_name)
                            print(f"Memeriksa file: {file_name}")  # Debug

                            # Cek jika file mengandung nama kategori
                            if kategori['nama'] in file_name.upper():
                                file_found = True  # Menandai bahwa kita menemukan file

                                # Membuat folder tujuan jika belum ada
                                tujuan_jenis_folder = os.path.join(folder_tujuan, kategori['folder'])
                                if not os.path.exists(tujuan_jenis_folder):
                                    os.makedirs(tujuan_jenis_folder)
                                    print(f"Folder jenis {kategori['folder']} dibuat di {folder_tujuan}.")

                                # Membuat folder NIP dalam folder jenis file
                                tujuan_nip_folder = os.path.join(tujuan_jenis_folder, nip)
                                if not os.path.exists(tujuan_nip_folder):
                                    os.makedirs(tujuan_nip_folder)
                                    print(f"Folder untuk NIP {nip} dibuat di {tujuan_jenis_folder}.")
                                else:
                                    print(f"Folder untuk NIP {nip} sudah ada, tidak membuat ulang.")

                                # Menyalin file ke folder NIP yang sesuai
                                target_file_path = os.path.join(tujuan_nip_folder, file_name)
                                if os.path.exists(target_file_path):
                                    print(f"File {file_name} sudah ada di {tujuan_nip_folder}, tidak menyalin.")
                                else:
                                    try:
                                        shutil.copy(file_path, tujuan_nip_folder)
                                        print(f"File {file_name} disalin ke {tujuan_nip_folder}.")
                                    except Exception as e:
                                        print(f"Error saat menyalin file {file_name}: {e}")

                        if not file_found:
                            print(f"Tidak ada file '{kategori['nama']}' ditemukan di NIP {nip}.")

        else:
            print(f"Folder instansi tidak ditemukan: {instansi_path}")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# Penggunaan fungsi
folder_inti = 'Z:\\SMKN3 MANADO\\Ananda'  # Pastikan path ini benar
folder_tanggal = os.path.join(folder_inti, '22-10-24')  # Pastikan folder ini ada
folder_smkn3 = 'Z:\\SMKN3 MANADO'  # Pastikan path ini benar
folder_tujuan = os.path.join(folder_smkn3, 'KLASIFIKASI')  # Folder tujuan di dalam SMKN3 MANADO

# Cek apakah folder_tanggal dan folder_tujuan ada
if not os.path.exists(folder_tanggal):
    print(f"Folder tanggal tidak ditemukan: {folder_tanggal}")
else:
    if not os.path.exists(folder_tujuan):
        os.makedirs(folder_tujuan)
        print(f"Folder tujuan dibuat: {folder_tujuan}")

    # Load kategori dari file JSON
    kategori_file_path = 'kategori_file.json'  # Pastikan path ini benar
    kategori_list = load_kategori(kategori_file_path)

    print("Memulai proses klasifikasi...")
    klasifikasikan_file(folder_tanggal, folder_tujuan, kategori_list)
    print("Proses klasifikasi selesai.")
