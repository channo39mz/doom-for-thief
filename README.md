# 🛡️ Anti-Reset OTP System (WinRE Protected)

## 📌 รายละเอียด
ระบบนี้จะ **ป้องกันไม่ให้ใครทำ Factory Reset เครื่อง** โดยไม่ใส่ OTP ที่ส่งผ่านอีเมล  
รันเมื่อผู้ใช้เข้าสู่ WinRE ผ่านเมนู `Advanced Startup > Restart Now`  
เหมาะสำหรับ: การป้องกันขโมย, โรงเรียน, โน๊ตบุคส่วนตัว

## 📁 โฟลเดอร์สำคัญ

| ชื่อไฟล์            | คำอธิบาย                             |
|---------------------|----------------------------------------|
| `mainprogram.py`    | โปรแกรมหลักที่ใช้ตรวจสอบ OTP         |
| `dist/mainprogram.exe` | ไฟล์ `.exe` ที่ build เสร็จแล้วจาก PyInstaller |
| `winpeshl.ini`      | ไฟล์ config ที่สั่งให้ WinRE รัน `.exe` โดยอัตโนมัติ |

## 🧰 สิ่งที่ต้องติดตั้งในเครื่องก่อน

- Python 3.x (เช่น 3.12)
- ติดตั้งไลบรารีที่ใช้:
  ```bash
  pip install smtplib email
  ```
- PyInstaller สำหรับ build:
  ```bash
  pip install pyinstaller
  ```

## 🛠️ ขั้นตอนการสร้าง .exe

1. **แก้ไขอีเมลและรหัสผ่านใน `mainprogram.py`:**
   ```python
   EMAIL_SENDER = "you@gmail.com"
   EMAIL_PASSWORD = "your_app_password"
   EMAIL_RECEIVER = "you@gmail.com"  # หรืออีเมลของมหาวิทยาลัย
   ```

2. **Build เป็น `.exe` แบบมี console:**
   ```bash
   pyinstaller --onefile mainprogram.py
   ```

3. ไฟล์จะอยู่ที่:
   ```
   ./dist/mainprogram.exe
   ```

## 🧩 ขั้นตอนการฝังลงใน WinRE

### 🔁 1. ค้นหา `winre.wim`

```bash
reagentc /info
```

ดูที่ `Windows RE location:` เช่น

```
\?\GLOBALROOT\device\harddisk0\partition4\Recovery\WindowsRE
```

### 🔗 2. Mount พาร์ทิชัน Recovery (หากยังไม่มี)

```bash
diskpart
```

ใน `diskpart`:

```bash
select disk 0
select partition 4
assign letter=R
exit
```

### 📂 3. Mount `winre.wim`

```bash
mkdir C:\WinREMount
dism /Mount-Wim /WimFile:R:\Recovery\WindowsRE\winre.wim /Index:1 /MountDir:C:\WinREMount
```

### 🧷 4. คัดลอก `.exe` และ `winpeshl.ini`

```bash
copy .\dist\mainprogram.exe C:\WinREMount\Windows\System32\
notepad C:\WinREMount\Windows\System32\winpeshl.ini
```

เพิ่มเนื้อหา:

```ini
[LaunchApp]
AppPath = %SYSTEMROOT%\System32\mainprogram.exe
```

### 💾 5. Commit กลับเข้า WinRE

```bash
dism /Unmount-Wim /MountDir:C:\WinREMount /Commit
```

## 🧪 การทดสอบระบบ

1. ไปที่:
   ```
   Settings > System > Recovery > Advanced Startup > Restart Now
   ```

2. เข้าสู่ WinRE
3. โปรแกรมจะรันและให้ใส่ OTP
4. หาก OTP ถูกต้อง → เปิดหน้า Reset
5. หาก OTP ผิด → Reset จะถูกบล็อค

## ⚠️ หมายเหตุความปลอดภัย

- โปรแกรมไม่สามารถทำงานได้หากไม่มีอินเทอร์เน็ต
- หาก OTP ไม่ถูกต้อง → ผู้ใช้จะไม่สามารถ reset ได้
- หาก OTP ถูก → systemreset.exe จะเปิด GUI สำหรับ reset
- ระบบนี้ไม่สามารถป้องกันการ format จาก external USB ได้

## ✅ สถานะ

| ฟีเจอร์                    | สถานะ    |
|----------------------------|----------|
| OTP ผ่านอีเมล             | ✅ สำเร็จ |
| ป้องกัน reset ไม่ได้ใส่ OTP | ✅ สำเร็จ |
| ทำงานใน WinRE             | ✅ สำเร็จ |
| Timeout & แจ้งเตือน fallback | 🔜 (optional) |