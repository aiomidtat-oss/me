#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ربات تلگرام کارشناس زیبایی و آرایشگری
مشاور شخصی شما برای زیبایی، آرایش و مراقبت از پوست و مو
"""

import asyncio
import sys
from telegram_bot import TelegramBot


def print_banner():
    """
    نمایش بنر شروع برنامه
    """
    banner = """
    ╭══════════════════════════════════════════════════════════════╮
    ║                💅 ربات کارشناس زیبایی و آرایشگری                ║
    ║                                                              ║
    ║        مشاور شخصی شما برای زیبایی و آرایش        ║
    ║                                                              ║
    ║  خدمات و مشاوره‌ها:                                        ║
    ║  • تشخیص نوع پوست و مو                                    ║
    ║  • مشاوره آرایش و زیبایی                                   ║
    ║  • راهکار مشکلات پوستی                                      ║
    ║  • مراقبت و نگهداری پوست و مو                            ║
    ║                                                              ║
    ╰══════════════════════════════════════════════════════════════╯
    """
    print(banner)


def print_instructions():
    """
    نمایش دستورالعمل‌های اولیه
    """
    instructions = """
    📋 دستورالعمل راه‌اندازی ربات آرایشگری:
    
    1️⃣ ابتدا فایل config.py را ویرایش کنید:
       • API_ID و API_HASH را از https://my.telegram.org دریافت کنید
       • شماره تلفن خود را وارد کنید
    
    2️⃣ بعد از تنظیمات، ربات را دوباره اجرا کنید
    
    3️⃣ کد تایید تلگرام را وارد کنید
    
    4️⃣ از مشاوره‌های زیبایی لذت ببرید! 💅
    
    💡 نکات مهم:
    • ربات فقط پیام‌های خصوصی (PV) را پردازش می‌کند
    • برای توقف ربات Ctrl+C فشار دهید
    • session فایل ذخیره می‌شود پس بار بعد نیازی به کد تایید نیست
    • از سوالات زیبایی و آرایشی بپرسید! 💄
    """
    print(instructions)


async def main():
    """
    تابع اصلی برنامه
    """
    print_banner()
    
    try:
        # ایجاد instance ربات
        bot = TelegramBot()
        
        # شروع ربات
        success = await bot.start()
        
        if success:
            print("✅ ربات با موفقیت اجرا شد!")
        else:
            print("❌ مشکل در راه‌اندازی ربات")
            print_instructions()
            
    except KeyboardInterrupt:
        print("\n👋 ربات توسط کاربر متوقف شد")
    except Exception as e:
        print(f"❌ خطای غیرمنتظره: {str(e)}")
        print("\n🔧 اگر مشکل ادامه داشت:")
        print("• فایل session را حذف کنید و دوباره تلاش کنید")
        print("• تنظیمات config.py را بررسی کنید")
        print("• از اتصال اینترنت مطمئن شوید")


def check_python_version():
    """
    بررسی نسخه پایتون
    """
    if sys.version_info < (3, 7):
        print("❌ این برنامه نیاز به Python 3.7 یا بالاتر دارد")
        print(f"نسخه فعلی شما: Python {sys.version}")
        sys.exit(1)


if __name__ == "__main__":
    # بررسی نسخه پایتون
    check_python_version()
    
    # اجرای ربات
    if sys.platform == 'win32':
        # برای ویندوز
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 خداحافظ!")
    except Exception as e:
        print(f"❌ خطای کلی: {str(e)}")
        input("\nEnter کلید را برای خروج فشار دهید...")
