import time
import os

# SQL sunucusu log dosyalarının yolu
log_dir = "/var/log/mysql/"

# İzlenecek anahtar kelimeler
keywords = ["failed", "error", "access denied"]

# Log dosyalarını izleme fonksiyonu
def watch_logs():
    # Log dosyalarının son erişim tarihini tutmak için bir sözlük oluştur
    log_files = {}
    while True:
        # Tüm log dosyalarını tarayın
        for filename in os.listdir(log_dir):
            # Sadece log dosyalarını seçin
            if not filename.endswith(".log"):
                continue
            # Dosyanın son erişim tarihini kontrol edin
            mtime = os.path.getmtime(log_dir + filename)
            if filename not in log_files:
                log_files[filename] = mtime
                continue
            # Dosya son erişim tarihi değişmişse
            if mtime > log_files[filename]:
                with open(log_dir + filename, "r") as f:
                    # Dosyadaki her satırı okuyun
                    for line in f.readlines():
                        # Anahtar kelimeleri içeren satırları filtreleyin
                        if any(keyword in line for keyword in keywords):
                            # Rapor dosyasına kaydedin
                            with open("report.txt", "a") as report_file:
                                report_file.write(line)
                log_files[filename] = mtime
        # Belirli bir aralıkta çalıştırın (örneğin, her 5 dakikada bir)
        time.sleep(300)

# Logları izlemek için fonksiyonu çağırın
watch_logs()
