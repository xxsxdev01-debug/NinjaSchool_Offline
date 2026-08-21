#!/bin/bash

# 1. Cấp quyền truy cập bộ nhớ
termux-setup-storage

# 2. Cập nhật và cài đặt các gói hỗ trợ
apk update
apk add git python3 py3-pip openjdk8 wget curl unzip ca-certificates

# 3. Cài đặt các thư viện Python
python3 -m pip install --upgrade pip
python3 -m pip install gdown licensing mysql-connector-python requests

# 4. Tải mã nguồn từ Repository trước
cd ~
rm -rf NinjaSchool_Offline
git clone https://github.com/xxsxdev01-debug/NinjaSchool_Offline

# 5. Di chuyển vào thư mục dự án
cd NinjaSchool_Offline 

# Tải file JAR đặt trực tiếp vào trong thư mục này luôn
JAR_URL="https://github.com/xxsxdev01-debug/DragonBall/releases/download/V1.1/NinjaSchoolOffline.jar"
echo -e "\033[1;36m[i] Đang tải NinjaSchoolOffline.jar trực tiếp vào thư mục dự án...\033[0m"
rm -f NinjaSchoolOffline.jar
wget -q --show-progress "$JAR_URL" -O NinjaSchoolOffline.jar

if [ ! -f "NinjaSchoolOffline.jar" ] || [ ! -s "NinjaSchoolOffline.jar" ]; then
    echo -e "\033[1;33m[!] Wget tải thất bại, đang thử lại bằng Curl...\033[0m"
    curl -L "$JAR_URL" -O NinjaSchoolOffline.jar
fi

# URL file data.zip
DATA_URL="https://github.com/xxsxdev01-debug/DragonBall/releases/download/V1.2/Data.zip"

echo -e "\033[1;36m[i] Đang tải dữ liệu Data từ Release...\033[0m"
wget -q --show-progress "$DATA_URL" -O data.zip || curl -L "$DATA_URL" -o data.zip

if [ -f "data.zip" ]; then
    echo -e "\033[1;32m[+] Đang giải nén dữ liệu game (700MB)...\033[0m"
    unzip -o data.zip
    rm data.zip
fi

# 6. Đưa các file khởi động vào hệ thống
chmod +x *.sh
cp *.sh $PREFIX/bin/

clear
echo -e "\033[1;32m==============================================="
echo -e "       CÀI ĐẶT HOÀN TẤT - HỆ THỐNG SẴN SÀNG       "
echo -e "===============================================\033[0m"

# 7. Đếm ngược 5 giây và TỰ ĐỘNG CHẠY
for i in {5..1}
do
    echo -ne "\033[1;33m[!] Tool sẽ tự khởi động sau $i giây...\r\033[0m"
    sleep 1
done

echo -e "\n\033[1;32m[+] Đang khởi chạy Tool NinjaSchool bằng Python3...\033[0m"

python3 menu.py
