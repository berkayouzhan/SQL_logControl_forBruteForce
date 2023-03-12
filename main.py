import time
import os

# SQL sunucusu log dosyalarının yolu # Path to SQL server log files
log_dir = "/var/log/mysql/"

# İzlenecek anahtar kelimeler # Keywords to watch
keywords = ["failed", "error", "access denied"]

# Log dosyalarını izleme fonksiyonu # Function to monitor log files
def watch_logs():
    # Log dosyalarının son erişim tarihini tutmak için bir sözlük oluştur # Create a dictionary to keep the last access date of log files
    log_files = {}
    while True:
        # Tüm log dosyalarını tarayın # Scan all log files
        for filename in os.listdir(log_dir):
            # Sadece log dosyalarını seçin # Select only log files
            if not filename.endswith(".log"):
                continue
            # Dosyanın son erişim tarihini kontrol edin # Check the last access date of the file
            mtime = os.path.getmtime(log_dir + filename)
            if filename not in log_files:
                log_files[filename] = mtime
                continue
            # Dosya son erişim tarihi değişmişse # If the file last access date has changed
            if mtime > log_files[filename]:
                with open(log_dir + filename, "r") as f:
                    # Dosyadaki her satırı okuyun # Read every line in the file
                    for line in f.readlines():
                        # Anahtar kelimeleri içeren satırları filtreleyin # Filter rows containing keywords
                        if any(keyword in line for keyword in keywords):
                            # Rapor dosyasına kaydedin # Save to report file
                            with open("report.txt", "a") as report_file:
                                report_file.write(line)
                log_files[filename] = mtime
        # Belirli bir aralıkta çalıştırın (örneğin, her 5 dakikada bir) # Run at a specified interval (for example, every 5 minutes)
        time.sleep(300)

# Logları izlemek için fonksiyonu çağırın # Call the function to watch the logs
watch_logs()
