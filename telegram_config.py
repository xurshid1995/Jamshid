# -*- coding: utf-8 -*-
"""
Telegram Bot Konfiguratsiya
Sozlamalar va konstantalar
"""

# Telegram bot sozlamalari
TELEGRAM_CONFIG = {
    # Bot asosiy sozlamalari
    'bot_name': 'Qarz Eslatmasi Bot',
    'bot_username': '@qarz_eslatma_bot',  # O'z bot username ingizni kiriting
    
    # Xabar yuborish sozlamalari
    'rate_limit': 1,  # Sekundiga 1 ta xabar
    'retry_attempts': 3,  # Qayta urinishlar soni
    'retry_delay': 5,  # Qayta urinish orasidagi kutish (sekund)
    
    # Qarz eslatmalari sozlamalari
    'daily_reminder_time': '10:00',  # Kunlik eslatmalar vaqti (HH:MM)
    'weekly_report_day': 1,  # Haftalik hisobot kuni (0=Yakshanba, 1=Dushanba, ...)
    'minimum_debt_amount': 1.0,  # Minimal qarz miqdori (USD)
    
    # Xabar shablonlari
    'templates': {
        'debt_reminder': {
            'emoji': '💰',
            'title': 'QARZ ESLATMASI',
            'include_date': True,
            'include_location': True
        },
        'payment_confirmation': {
            'emoji': '✅',
            'title': 'TO\'LOV QABUL QILINDI',
            'include_remaining': True
        },
        'daily_summary': {
            'emoji': '📊',
            'title': 'KUNLIK HISOBOT'
        },
        'weekly_report': {
            'emoji': '📈',
            'title': 'HAFTALIK HISOBOT'
        }
    },
    
    # Xabar limitleri
    'max_message_length': 4096,  # Telegram limit
    'max_debts_per_message': 20,  # Bir xabarda maksimal qarzlar soni
}


# Xabar formatlash funksiyalari
def format_currency_usd(amount: float) -> str:
    """USD formatini qaytarish"""
    return f"${amount:,.2f}"


def format_currency_uzs(amount: float) -> str:
    """UZS formatini qaytarish"""
    return f"{amount:,.0f} so'm"


def format_phone(phone: str) -> str:
    """Telefon raqamini formatlash"""
    if not phone:
        return "Telefon yo'q"
    
    # +998 90 123 45 67 formatiga keltirish
    clean = ''.join(filter(str.isdigit, phone))
    if len(clean) == 12 and clean.startswith('998'):
        return f"+{clean[:3]} {clean[3:5]} {clean[5:8]} {clean[8:10]} {clean[10:]}"
    elif len(clean) == 9:
        return f"+998 {clean[:2]} {clean[2:5]} {clean[5:7]} {clean[7:]}"
    else:
        return phone


def format_datetime(dt) -> str:
    """Sana va vaqtni formatlash"""
    if not dt:
        return ""
    return dt.strftime('%d.%m.%Y %H:%M')


def format_date(dt) -> str:
    """Sanani formatlash"""
    if not dt:
        return ""
    return dt.strftime('%d.%m.%Y')


# Logging konfiguratsiyasi
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': 'logs/telegram_bot.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        }
    },
    'loggers': {
        'telegram_bot': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False
        },
        'debt_scheduler': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    }
}


# Xato xabarlari
ERROR_MESSAGES = {
    'bot_not_initialized': '❌ Bot ishga tushmagan. TELEGRAM_BOT_TOKEN ni tekshiring.',
    'customer_not_found': '❌ Mijoz topilmadi.',
    'no_telegram_id': '⚠️ Mijoz uchun Telegram ID mavjud emas.',
    'send_failed': '❌ Xabar yuborishda xatolik yuz berdi.',
    'db_error': '❌ Ma\'lumotlar bazasida xatolik.',
    'invalid_phone': '❌ Telefon raqami noto\'g\'ri formatda.',
}


# Muvaffaqiyat xabarlari
SUCCESS_MESSAGES = {
    'reminder_sent': '✅ Qarz eslatmasi yuborildi',
    'payment_confirmed': '✅ To\'lov tasdiqlanganligini bildirish yuborildi',
    'report_sent': '✅ Hisobot yuborildi',
    'scheduler_started': '✅ Avtomatik eslatmalar ishga tushdi',
}


# Help matnlar
HELP_TEXTS = {
    'start': (
        "Assalomu alaykum! 👋\n\n"
        "Bu qarz eslatmalari botidir.\n"
        "Qarzingizni tekshirish va to'lash uchun tugmalardan foydalaning."
    ),
    'commands': (
        "📱 <b>Bot buyruqlari:</b>\n\n"
        "/start - Botni boshlash\n"
        "/help - Yordam\n"
        "/mydebt - Qarzimni ko'rish\n"
        "/history - To'lovlar tarixi\n"
        "/contact - Bog'lanish"
    ),
    'contact': (
        "📞 <b>Bog'lanish</b>\n\n"
        "Savollar yoki muammolar uchun:\n"
        "📱 Telefon: +998 XX XXX XX XX\n"
        "📧 Email: info@example.uz\n"
        "🕒 Ish vaqti: 09:00 - 18:00"
    )
}


# Admin panel sozlamalari
ADMIN_CONFIG = {
    'commands': [
        {'command': '/stats', 'description': 'Statistika'},
        {'command': '/debts', 'description': 'Barcha qarzlar'},
        {'command': '/sendall', 'description': 'Hammaga xabar yuborish'},
        {'command': '/export', 'description': 'Qarzlarni export qilish'},
    ],
    'export_formats': ['CSV', 'Excel', 'PDF'],
    'stats_update_interval': 3600,  # Soatiga 1 marta yangilanish
}


# Mijoz o'zaro muloqot sozlamalari
CUSTOMER_FEATURES = {
    'can_check_debt': True,  # Qarzni tekshirish
    'can_view_history': True,  # Tarixni ko'rish
    'can_request_reminder': False,  # Eslatma so'rash
    'can_send_feedback': True,  # Fikr-mulohaza yuborish
}


if __name__ == "__main__":
    # Test
    print("📋 Telegram Bot Configuration")
    print(f"Bot name: {TELEGRAM_CONFIG['bot_name']}")
    print(f"Daily reminder: {TELEGRAM_CONFIG['daily_reminder_time']}")
    print(f"Minimum debt: ${TELEGRAM_CONFIG['minimum_debt_amount']}")
    
    # Test formatters
    print("\n💵 Currency formatting:")
    print(f"USD: {format_currency_usd(1234.56)}")
    print(f"UZS: {format_currency_uzs(16049280)}")
    
    print("\n📱 Phone formatting:")
    print(format_phone("998901234567"))
    print(format_phone("901234567"))
