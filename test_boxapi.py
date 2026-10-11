#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
تست ساده برای بررسی پاسخ BoxAPI
"""

from box_api_client import BoxAPIClient

def main():
    print("🧪 شروع تست BoxAPI...")
    
    # ایجاد کلاینت
    client = BoxAPIClient()
    
    # تست پیام ساده
    print("\n" + "="*50)
    print("تست 1: پیام ساده فارسی")
    print("="*50)
    
    response = client.send_message("سلام چطوری؟")
    print(f"پاسخ نهایی: {response}")
    
    print("\n" + "="*50)
    print("تست 2: پیام انگلیسی")
    print("="*50)
    
    response = client.send_message("Hello, how are you?")
    print(f"پاسخ نهایی: {response}")

if __name__ == "__main__":
    main()
