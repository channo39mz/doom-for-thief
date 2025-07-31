import subprocess
import os
import sys
import time

def run_cmd(cmd, shell=False):
    print(f"[RUN] {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        subprocess.run(cmd, check=True, shell=shell)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed: {e}")
        sys.exit(1)

def main():
    mount_dir = "C:\\WinREMount"
    wim_path = "R:\\Recovery\\WindowsRE\\winre.wim"
    system32_path = os.path.join(mount_dir, "Windows", "System32")
    exe_name = "mainprogram.exe"
    ini_name = "winpeshl.ini"

    print("=== 🛡️ Anti-Reset OTP Installer ===")
    input("⚠️ กรุณารันโปรแกรมนี้ด้วยสิทธิ Administrator แล้วกด Enter เพื่อติดตั้ง...")

    print("[1] Assigning drive letter R: to Recovery Partition...")
    with open("diskpart_script.txt", "w") as f:
        f.write("select disk 0\nselect partition 4\nassign letter=R\nexit\n")
    run_cmd(["diskpart", "/s", "diskpart_script.txt"])

    print("[2] สร้างโฟลเดอร์ mount...")
    os.makedirs(mount_dir, exist_ok=True)

    print("[3] Mount winre.wim ...")
    run_cmd([
        "dism", "/Mount-Wim",
        f"/WimFile={wim_path}",
        "/Index:1",
        f"/MountDir={mount_dir}"
    ])

    print("[4] คัดลอก mainprogram.exe และ winpeshl.ini เข้า WinRE ...")
    run_cmd(["copy", exe_name, os.path.join(system32_path, "")], shell=True)
    run_cmd(["copy", ini_name, os.path.join(system32_path, "")], shell=True)

    print("[5] Commit กลับเข้า winre.wim ...")
    run_cmd([
        "dism", "/Unmount-Wim",
        f"/MountDir={mount_dir}",
        "/Commit"
    ])

    print("[6] ลบ drive letter R: (ไม่จำเป็น แต่เพื่อความเรียบร้อย)")
    with open("diskpart_remove.txt", "w") as f:
        f.write("select disk 0\nselect partition 4\nremove letter=R\nexit\n")
    run_cmd(["diskpart", "/s", "diskpart_remove.txt"])

    print("\n✅ ติดตั้งเสร็จสิ้น! เครื่องของคุณป้องกัน Reset แล้วเรียบร้อย 🎉")
    time.sleep(3)

if __name__ == "__main__":
    main()