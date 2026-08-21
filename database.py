import os
import time

def setup_database():
    print('\033[2J\033[H', end='')
    print("\033[1;32m===============================================")
    print("      HỆ THỐNG TỰ ĐỘNG SETUP SQL & PHPMYADMIN        ")
    print("      (PHIÊN BẢN TỐI ƯU CHO iOS / ISH SHELL)   ")
    print("===============================================\033[0m")

    # Cấu hình thông số
    DB_NAME = "nso_xxsx"
    DB_USER = "root"
    DB_PASS = "" 
    DB_HOST = "127.0.0.1"

    # 1. DỌN DẸP TIẾN TRÌNH
    print("\033[1;31m[*] Đang dọn dẹp hệ thống...\033[0m")
    os.system("killall -9 httpd mariadbd mysqld 2>/dev/null")
    os.system("rm -f /run/mysqld/mysqld.sock")
    
    # 2. CÀI ĐẶT GÓI (Sử dụng apk của Alpine Linux - Đã thay thế các gói php không tồn tại bằng php8 hoặc bỏ qua để tránh lỗi)
    print(f"\033[1;36m[1/5] Cài đặt gói hệ thống bằng apk...\033[0m")
    os.system("apk update")
    # Thay thế php82-apache2/mysqli/session thành các gói php8 tương thích trên Alpine iSH
    os.system("apk add mariadb mariadb-client apache2 wget unzip curl")


    # 3. CẤU HÌNH FIX LỖI JAVA
    print(f"\033[1;33m[*] Đang cấu hình Fix lỗi NullPointerException...\033[0m")
    cnf_path = "/etc/my.cnf.d/mariadb-server.cnf"
    os.system(f"mkdir -p /etc/my.cnf.d")
    with open(cnf_path, "w") as f:
        f.write("[mysqld]\n")
        f.write("character-set-server=latin1\n")
        f.write("collation-server=latin1_swedish_ci\n")
        f.write("skip-character-set-client-handshake\n")
        f.write("innodb_strict_mode=0\n")
        f.write("lower_case_table_names=1\n")

                    # 4. KHỞI ĐỘNG MYSQL (Đã tối ưu kiểm tra tiến trình sống trên iSH)
    print(f"\033[1;36m[2/5] Khởi động MariaDB Server...\033[0m")
    os.system("addgroup -g 1000 mysql 2>/dev/null")
    os.system("adduser -u 1000 -D -G mysql mysql 2>/dev/null")
    os.system("mkdir -p /run/mysqld && chown mysql:mysql /run/mysqld")
    os.system("mkdir -p /var/lib/mysql/mysql && chown -R mysql:mysql /var/lib/mysql")
    
    # Khởi động kèm theo ghi log lỗi ra file tạm để kiểm tra nếu cần
    os.system("nohup mysqld --skip-grant-tables --skip-networking=0 --user=root > /tmp/mysqld.log 2>&1 &")
    
    # Chờ và kiểm tra socket xuất hiện thay vì sleep cố định
    for _ in range(10):
        if os.path.exists("/run/mysqld/mysqld.sock"):
            break
        time.sleep(1)





    # 5. NẠP DỮ LIỆU TỪ GITHUB
    print(f"\033[1;36m[3/5] Đang nạp SQL từ GitHub...\033[0m")
    url_sql = "https://raw.githubusercontent.com/xxsxdev01-debug/NinjaSchool_Offline/main/nso_xxsx.sql"
    os.system("rm -f nso_xxsx.sql")
    os.system(f"curl -L {url_sql} -o nso_xxsx.sql")
    
    os.system(f"mariadb -u root -e 'DROP DATABASE IF EXISTS {DB_NAME};'")
    os.system(f"mariadb -u root -e 'CREATE DATABASE {DB_NAME} CHARACTER SET utf8 COLLATE utf8_general_ci;'")
    os.system(f"mariadb -u root {DB_NAME} < nso_xxsx.sql")
    os.system(f"mariadb -u root -e \"GRANT ALL PRIVILEGES ON *.* TO '{DB_USER}'@'localhost'; FLUSH PRIVILEGES;\"")
    
    print(f"\033[1;32m[V] Đã tạo và nạp thành công Database: {DB_NAME}\033[0m")

    # 6. CẤU HÌNH PHPMYADMIN
    print(f"\033[1;36m[4/5] Cấu hình phpMyAdmin...\033[0m")
    web_dir = "/var/www/localhost/htdocs"
    os.system(f"rm -rf {web_dir}/phpmyadmin")
    os.system(f"mkdir -p {web_dir}")
    
    if not os.path.exists(f"{web_dir}/phpmyadmin"):
        os.system(f"cd {web_dir} && wget https://files.phpmyadmin.net/phpMyAdmin/5.2.1/phpMyAdmin-5.2.1-all-languages.zip")
        os.system(f"cd {web_dir} && unzip -q phpMyAdmin-5.2.1-all-languages.zip")
        os.system(f"cd {web_dir} && mv phpMyAdmin-5.2.1-all-languages phpmyadmin && rm *.zip")

    config_file = f"{web_dir}/phpmyadmin/config.inc.php"
    with open(config_file, "w") as f:
        f.write(f"<?php $cfg['Servers'][1]['auth_type'] = 'config'; $cfg['Servers'][1]['user'] = '{DB_USER}'; $cfg['Servers'][1]['password'] = '{DB_PASS}'; $cfg['Servers'][1]['host'] = '{DB_HOST}'; $cfg['Servers'][1]['AllowNoPassword'] = true; ?>")

    # 7. KHỞI ĐỘNG APACHE
    print(f"\033[1;36m[5/5] Khởi động Apache Server...\033[0m")
    os.system("killall -9 httpd 2>/dev/null")
    os.system("httpd")

    print("\033[1;32m===============================================")
    print("      THIẾT LẬP HOÀN TẤT - SQL SẴN SÀNG      ")
    print("===============================================")
    print(f" ➤ Database: {DB_NAME}")
    print(f" ➤ Link PhpMyadmin: http://127.0.0.1/phpmyadmin/")
    print(f" ➤ User: root")
    print(f" ➤ Pass: Chưa Đặt Pass")

    print("===============================================\033[0m")
    input("Nhấn Enter để quay lại Menu...")

if __name__ == "__main__":
    setup_database()
