import os
import csv
import re

if not os.path.exists("database.csv") or not os.path.exists("index.html"):
    print("Error: Berkas database.csv atau index.html lama tidak ditemukan di folder ini!")
    exit()

print("Membaca database Excel baru Anda...")
with open("database.csv", "r", encoding="utf-8-sig") as f:
    sample = f.read(2048)
    pemisah = ';' if ';' in sample else ','

# Ambil data tombol 3 yang baru dari excel
link3_baru_list = []
with open("database.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=pemisah)
    for row in reader:
        cleaned_row = {k.strip().lower() if k else '': v.strip() for k, v in row.items()}
        link3 = next((v for k, v in cleaned_row.items() if 'tombol3' in k), '').strip()
        if link3:
            link3_baru_list.append(link3)

print("Membaca dan memproses file index.html lama...")
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Pola untuk mencari baris token dan link di dalam javascript index.html
# Contoh: "token": { t1: "...", t2: "...", t3: "..." }
pattern = r'(\s*"[^"]+"\s*:\s*\{\s*t1\s*:\s*"[^"]+"\s*,\s*t2\s*:\s*"[^"]+"\s*,\s*t3\s*:\s*")([^"]+)("\s*\}\s*,?)'

matches = list(re.finditer(pattern, html_content))

if len(matches) == 0:
    print("Error: Format database di dalam index.html tidak dikenali atau kosong!")
    exit()

# Lakukan penggantian t3 dari bawah ke atas agar indeks karakter tidak bergeser
modifikasi_html = html_content
update_count = 0

for i, match in enumerate(matches):
    if i < len(link3_baru_list):
        link3_baru = link3_baru_list[i]
        # Cari posisi teks asli di dalam string html
        start_idx = match.start()
        end_idx = match.end()
        
        # Susun ulang baris tersebut dengan mengganti nilai t3 saja
        baris_lama = match.group(0)
        # Ganti bagian t3:"..." dengan link baru
        baris_baru = re.sub(r'(t3\s*:\s*")[^"]+(")', r'\g<1>' + link3_baru + r'\g<2>', baris_lama)
        
        # Lakukan replacement spesifik pada teks tersebut
        modifikasi_html = modifikasi_html.replace(baris_lama, baris_baru, 1)
        update_count += 1

# Tulis kembali ke file index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(modifikasi_html)

print(f"\n💥 BERHASIL SINKRONISASI BOSKU! 💥")
print(f"-> Berhasil memperbarui {update_count} link Tombol 3.")
print(f"-> Token lama Anda tetap AMAN dan tidak berubah sama sekali di index.html.")
