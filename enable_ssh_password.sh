#!/bin/bash
# SSH Password Authentication'ni yoqish
# Serverda root yoki sudo huquqi bilan bajarish kerak

echo "🔧 SSH Password Authentication'ni yoqish..."
echo ""

# Backup yaratish
echo "📋 Backup yaratilmoqda..."
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup.$(date +%Y%m%d_%H%M%S)

# SSH config'ni o'zgartirish
echo "✏️ SSH konfiguratsiyasi o'zgartrilmoqda..."

# PasswordAuthentication'ni yoqish
sudo sed -i 's/^#*PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
sudo sed -i 's/^#*PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Agar PasswordAuthentication qatori bo'lmasa, qo'shish
if ! grep -q "^PasswordAuthentication" /etc/ssh/sshd_config; then
    echo "PasswordAuthentication yes" | sudo tee -a /etc/ssh/sshd_config
fi

# PubkeyAuthentication ham yoqilgan bo'lishi uchun
sudo sed -i 's/^#*PubkeyAuthentication no/PubkeyAuthentication yes/' /etc/ssh/sshd_config
sudo sed -i 's/^#*PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config

if ! grep -q "^PubkeyAuthentication" /etc/ssh/sshd_config; then
    echo "PubkeyAuthentication yes" | sudo tee -a /etc/ssh/sshd_config
fi

# ChallengeResponseAuthentication ham yoqish
sudo sed -i 's/^#*ChallengeResponseAuthentication no/ChallengeResponseAuthentication yes/' /etc/ssh/sshd_config

# Konfiguratsiyani tekshirish
echo ""
echo "📊 Yangi konfiguratsiya:"
echo "----------------------"
grep "^PasswordAuthentication" /etc/ssh/sshd_config
grep "^PubkeyAuthentication" /etc/ssh/sshd_config
echo "----------------------"
echo ""

# SSH syntax'ni tekshirish
echo "🔍 SSH konfiguratsiya syntax'ni tekshirish..."
sudo sshd -t

if [ $? -eq 0 ]; then
    echo "✅ Konfiguratsiya syntax to'g'ri"
    echo ""
    echo "🔄 SSH servisini qayta ishga tushirish..."
    sudo systemctl restart sshd
    
    if [ $? -eq 0 ]; then
        echo "✅ SSH servisi muvaffaqiyatli qayta ishga tushdi!"
        echo ""
        echo "🎉 Password authentication yoqildi!"
        echo "💡 Endi 'ssh jamshid@139.59.154.185' bilan parol orqali ulanishingiz mumkin"
    else
        echo "❌ SSH servisini qayta ishga tushirishda xatolik!"
        echo "🔙 Backup'dan tiklash: sudo cp /etc/ssh/sshd_config.backup.* /etc/ssh/sshd_config"
    fi
else
    echo "❌ SSH konfiguratsiyada xatolik bor!"
    echo "🔙 Backup'dan tiklash: sudo cp /etc/ssh/sshd_config.backup.* /etc/ssh/sshd_config"
fi
