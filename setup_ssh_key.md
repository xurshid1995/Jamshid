# SSH Kalit Autentifikatsiyasini Sozlash

## Windows'da SSH Kalit Yaratish va Serverga O'rnatish

### 1. SSH Kalit Juftligini Yaratish (Windows PowerShell)

```powershell
# SSH kalit generatsiya qilish
ssh-keygen -t ed25519 -C "deploy@jamshid"

# Enter tugmasini bosib default joylashuvni qabul qiling: C:\Users\YourUsername\.ssh\id_ed25519
# Parolni bo'sh qoldiring (Enter bosing) - avtomatik deploy uchun
```

### 2. Public Kalitni Nusxa Olish

```powershell
# Public kalitni ko'rish
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
```

### 3. Server'ga Public Kalitni Qo'shish

PuTTY orqali server'ga ulaning:
- Host: 139.59.154.185
- User: root
- Password: Teleport7799

Server'da quyidagi buyruqlarni bajaring:

```bash
# .ssh papkasini yaratish (agar yo'q bo'lsa)
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# authorized_keys faylini yaratish
touch ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Public kalitni qo'shish (Windows'dan nusxa olingan kalitni qo'ying)
echo "sizning-public-kalit-matin" >> ~/.ssh/authorized_keys
```

### 4. SSH Ulanishni Tekshirish

Windows PowerShell'da:

```powershell
# Endi parolsiz ulanish ishlashi kerak
ssh root@139.59.154.185 "echo 'SSH kalit ishladi!'"
```

### 5. Avtomatik Deploy Script

Kalit sozlangandan keyin deploy script ishlaydi:

```powershell
# Bir buyruqda deploy
ssh root@139.59.154.185 "cd /var/www/jamshid && git pull origin main && systemctl restart jamshid && systemctl status jamshid --no-pager"
```

## Muqobil Yechim: SSH Config Fayli

`C:\Users\YourUsername\.ssh\config` faylini yarating:

```
Host jamshid-server
    HostName 139.59.154.185
    User root
    IdentityFile ~/.ssh/id_ed25519
    StrictHostKeyChecking no
```

Keyin oddiy buyruq bilan ulaning:

```powershell
ssh jamshid-server "cd /var/www/jamshid && git pull && systemctl restart jamshid"
```

## Tezkor Yechim: Birinchi Marta Qabul Qilish

Agar SSH kalit o'rnatish vaqt oladigan bo'lsa, kamida birinchi marta qo'lda ulaning:

```powershell
# Birinchi marta ulanish - kalitni qabul qiladi
ssh root@139.59.154.185

# "yes" deb yozing va Enter bosing
# Keyin parol: Teleport7799
# exit deb chiqing

# Endi keyingi safar ishlaydi
ssh root@139.59.154.185 -o PreferredAuthentications=password -o PubkeyAuthentication=no "cd /var/www/jamshid && git pull origin main && systemctl restart jamshid"
```
