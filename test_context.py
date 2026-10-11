#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
تست قابلیت context در BoxAPI
"""

from box_api_client import BoxAPIClient

def main():
    print("🧪 شروع تست قابلیت Context...")
    
    # ایجاد کلاینت
    client = BoxAPIClient()
    
    # شبیه‌سازی پیام‌های قبلی
    fake_history = [
        {"role": "user", "content": "سلام! اسم من علی هست"},
        {"role": "assistant", "content": "سلام علی عزیز! خوشحالم آشناتون شدم 😊"},
        {"role": "user", "content": "من دانشجوی کامپیوتر هستم"},
        {"role": "assistant", "content": "واو! رشته خفنی انتخاب کردی علی 💻"},
        {"role": "user", "content": "چند سالمه؟"},
    ]
    
    print("\n" + "="*60)
    print("تست 1: پیام بدون context")
    print("="*60)
    
    response = client.send_message("چند سالمه؟")
    print(f"پاسخ بدون context: {response}")
    
    print("\n" + "="*60)
    print("تست 2: پیام با context (باید اسم کاربر را به یاد داشته باشد)")
    print("="*60)
    
    response = client.send_message_with_context("چند سالمه؟", fake_history)
    print(f"پاسخ با context: {response}")
    
    print("\n" + "="*60)
    print("تست 3: پیام دنباله‌دار با context")
    print("="*60)
    
    # اضافه کردن پیام جدید به تاریخچه
    fake_history.extend([
        {"role": "assistant", "content": response},
        {"role": "user", "content": "رشته من چی بود؟"}
    ])
    
    response = client.send_message_with_context("رشته من چی بود؟", fake_history)
    print(f"پاسخ دوم با context: {response}")

if __name__ == "__main__":
    main()
