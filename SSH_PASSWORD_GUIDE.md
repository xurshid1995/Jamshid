# SSH Password Authentication'ni yoqish bo'yicha qo'llanma

## ❓ Muammo
PowerShell'dan `ssh jamshid@139.59.154.185` orqali ulanishda "Permission denied (publickey)" xatosi.

**Sabab:** Server faqat SSH key autentifikatsiyasini qabul qiladi, parol bilan ulanish o'chirilgan.

---

## ✅ Yechim: Password Authentication'ni yoqish

### 1️⃣ Serverga kirish (birinchi marta)

**PuTTY orqali:**
- Yuklab olish: https://www.putty.org/
- Host: `139.59.154.185`
- Port: `22`
- Username: `jamshid`
- Password: `Teleport7799`

**Yoki boshqa SSH client:**
- MobaXterm
- Git Bash
- WSL (Windows Subsystem for Linux)

### 2️⃣ Serverda quyidagi komandalarni bajaring:

```bash
# 1. Skriptni serverga yuklash (yoki qo'lda yozish)
wget https://raw.githubusercontent.com/YOUR_REPO/enable_ssh_password.sh
# yoki
nano enable_ssh_password.sh  # paste script content

# 2. Ruxsat berish
chmod +x enable_ssh_password.sh

# 3. Bajarish
sudo ./enable_ssh_password.sh
```

### 3️⃣ Yoki qo'lda o'zgartirish:

```bash
# SSH config faylini ochish
sudo nano /etc/ssh/sshd_config

# Quyidagi qatorlarni topib o'zgartiring:
PasswordAuthentication yes
PubkeyAuthentication yes
ChallengeResponseAuthentication yes

# Saqlash: Ctrl+O, Enter, Ctrl+X

# SSH'ni restart qilish
sudo systemctl restart sshd

# Status tekshirish
sudo systemctl status sshd
```

### 4️⃣ Test qilish

Yangi PowerShell oynasida:
```powershell
ssh jamshid@139.59.154.185
# Parol so'ralishi kerak: Teleport7799
```

---

## 🔐 Xavfsizlik eslatma

Password authentication yoqilganda server brute-force hujumlarga ochiq bo'ladi. 

**Tavsiya:**
1. ✅ Kuchli parol ishlating
2. ✅ Fail2ban o'rnating (kirish urinishlarini cheklaydi)
3. ✅ SSH portini o'zgartiring (22 o'rniga boshqa)
4. ✅ SSH key ham yoqilgan bo'lsin (ikkalasi birgalikda)

**Fail2ban o'rnatish:**
```bash
sudo apt update
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## 🚀 Keyin avtomatik deploy

Password authentication yoqilgandan so'ng, PowerShell'dan to'g'ridan-to'g'ri deploy qilishingiz mumkin:

```powershell
# Windows'da sshpass o'rnating (parolni avtomatik berish uchun)
# yoki Git Bash ishlatish mumkin

# Git Bash'da:
sshpass -p 'Teleport7799' ssh jamshid@139.59.154.185 'cd /var/www/jamshid && git pull origin main && sudo systemctl restart jamshid'
```

Yoki interaktiv ravishda:
```powershell
ssh jamshid@139.59.154.185
# Parol: Teleport7799
cd /var/www/jamshid
git pull origin main
sudo systemctl restart jamshid
```

---

## 📝 Fayllar

- `enable_ssh_password.sh` - Avtomatik konfiguratsiya skripti
- `deploy_manual.sh` - Qo'lda deploy qilish skripti

---

**Maslahat:** Bir marta SSH key'ni ham to'g'ri qo'shib oling, keyin parolsiz ishlaysiz! 🎉
