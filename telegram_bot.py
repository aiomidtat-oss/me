import asyncio
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from box_api_client import BoxAPIClient
from config import API_ID, API_HASH, PHONE_NUMBER, SESSION_NAME


class TelegramBot:
    def __init__(self):
        self.api_id = API_ID
        self.api_hash = API_HASH
        self.phone_number = PHONE_NUMBER
        self.session_name = SESSION_NAME
        self.client = None
        self.box_api = BoxAPIClient()
        self.authorized_users = set()  # لیست کاربران مجاز
        self.conversation_history = {}  # تاریخچه گفتگو برای هر کاربر
        
    async def start(self):
        """
        شروع ربات و اتصال به تلگرام
        """
        print("🚀 در حال راه‌اندازی ربات کارشناس زیبایی...")
        
        # بررسی تنظیمات
        if not self._validate_config():
            return False
            
        # ایجاد کلاینت تلگرام
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)
        
        try:
            # اتصال به تلگرام
            await self.client.start()
            print("✅ اتصال به تلگرام برقرار شد")
            
            # بررسی اینکه آیا وارد شده‌ایم یا نه
            if not await self.client.is_user_authorized():
                await self._login()
            
            # تست اتصال به BoxAPI
            print("🧪 در حال تست اتصال به BoxAPI...")
            if not self.box_api.test_connection():
                print("❌ مشکل در اتصال به BoxAPI - ربات ممکن است درست کار نکند")
            
            # راه‌اندازی handler پیام‌ها
            self._setup_handlers()
            
            print("🎉 ربات کارشناس زیبایی آماده مشاوره است!")
            print("💅 از من سوالات زیبایی، آرایش و مراقبت پوست بپرسید!")
            print("💡 برای توقف ربات، Ctrl+C را فشار دهید")
            
            # نگه داشتن ربات زنده
            await self.client.run_until_disconnected()
            
        except KeyboardInterrupt:
            print("\n🛑 ربات توسط کاربر متوقف شد")
        except Exception as e:
            print(f"❌ خطا در راه‌اندازی ربات: {str(e)}")
            return False
        finally:
            if self.client:
                await self.client.disconnect()
                print("👋 اتصال قطع شد")
        
        return True
    
    def _validate_config(self):
        """
        بررسی صحت تنظیمات
        """
        if (self.api_id == 'YOUR_API_ID' or 
            self.api_hash == 'YOUR_API_HASH' or 
            self.phone_number == 'YOUR_PHONE_NUMBER'):
            print("❌ لطفاً ابتدا اطلاعات API را در فایل config.py وارد کنید")
            print("📖 برای دریافت API_ID و API_HASH به https://my.telegram.org مراجعه کنید")
            return False
        return True
    
    async def _login(self):
        """
        ورود به تلگرام با شماره تلفن و کد تایید
        """
        try:
            print(f"📱 در حال ارسال کد تایید به شماره: {self.phone_number}")
            await self.client.send_code_request(self.phone_number)
            
            # دریافت کد تایید از کاربر
            code = input("🔐 کد تایید دریافتی را وارد کنید: ").strip()
            
            try:
                await self.client.sign_in(self.phone_number, code)
                print("✅ ورود موفقیت‌آمیز!")
                
            except SessionPasswordNeededError:
                # اگر Two-Factor Authentication فعال باشد
                password = input("🔒 رمز دو مرحله‌ای (2FA) را وارد کنید: ").strip()
                await self.client.sign_in(password=password)
                print("✅ ورود با رمز دو مرحله‌ای موفقیت‌آمیز!")
                
        except Exception as e:
            print(f"❌ خطا در فرآیند ورود: {str(e)}")
            raise
    
    def _setup_handlers(self):
        """
        تنظیم handler های مختلف پیام
        """
        @self.client.on(events.NewMessage(incoming=True))
        async def message_handler(event):
            await self._handle_message(event)
    
    async def _get_recent_messages(self, chat_id, limit=10):
        """
        دریافت 10 پیام آخر برای context بهتر
        """
        try:
            messages = []
            async for message in self.client.iter_messages(chat_id, limit=limit):
                if message.message:  # فقط پیام‌های تکستی
                    # مشخص کردن فرستنده
                    sender_name = "User" if message.out else "Bot"
                    messages.append({
                        "role": "assistant" if message.out else "user",
                        "content": message.message,
                        "sender": sender_name
                    })
            
            # مرتب کردن پیام‌ها به ترتیب زمانی درست
            messages.reverse()
            return messages
            
        except Exception as e:
            print(f"❌ خطا در دریافت پیام‌های قبلی: {str(e)}")
            return []
    
    def _update_conversation_history(self, user_id, user_message, bot_response):
        """
        به‌روزرسانی تاریخچه گفتگو
        """
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # اضافه پیام کاربر
        self.conversation_history[user_id].append({
            "role": "user",
            "content": user_message
        })
        
        # اضافه پاسخ ربات
        self.conversation_history[user_id].append({
            "role": "assistant", 
            "content": bot_response
        })
        
        # نگه داشتن فقط 20 پیام آخر (10 رفت و برگشت)
        if len(self.conversation_history[user_id]) > 20:
            self.conversation_history[user_id] = self.conversation_history[user_id][-20:]

    async def _handle_message(self, event):
        """
        پردازش پیام‌های دریافتی با context 10 پیام آخر
        """
        try:
            # فقط پیام‌های خصوصی (PV) را پردازش می‌کنیم
            if not event.is_private:
                return
                
            sender = await event.get_sender()
            message_text = event.message.message
            user_id = sender.id
            
            # نادیده گرفتن پیام‌های خالی
            if not message_text or not message_text.strip():
                return
            
            print(f"📨 پیام دریافتی از {sender.first_name} (@{sender.username}): {message_text[:100]}...")
            
            # ارسال پیام "در حال تایپ" 
            async with self.client.action(event.chat_id, 'typing'):
                # دریافت 10 پیام آخر برای context
                print(f"🔍 در حال دریافت 10 پیام آخر برای context...")
                recent_messages = await self._get_recent_messages(event.chat_id, 10)
                
                # ارسال پیام با context به BoxAPI
                ai_response = self.box_api.send_message_with_context(message_text, recent_messages)
                
                # به‌روزرسانی تاریخچه گفتگو
                self._update_conversation_history(user_id, message_text, ai_response)
                
                # ارسال پاسخ به کاربر
                await event.reply(ai_response)
                
            print(f"✅ پاسخ با context ارسال شد به {sender.first_name}")
            
        except Exception as e:
            print(f"❌ خطا در پردازش پیام: {str(e)}")
            try:
                # ارسال پیام خطا به کاربر
                error_message = "ببخشید عزیزم! یه مشکل فنی پیش اومده و نتونستم به سوال زیباییت جواب بدم 😅 لطفاً دوباره امتحان کن جانم 💅"
                await event.reply(error_message)
            except:
                pass  # اگر حتی پیام خطا هم نتوان ارسال کرد
    
    async def stop(self):
        """
        توقف ربات
        """
        if self.client:
            await self.client.disconnect()
            print("🛑 ربات متوقف شد")
    
    async def send_message_to_user(self, username_or_id, message):
        """
        ارسال پیام به کاربر خاص (برای تست یا کاربردهای خاص)
        """
        try:
            await self.client.send_message(username_or_id, message)
            print(f"✅ پیام به {username_or_id} ارسال شد")
            return True
        except Exception as e:
            print(f"❌ خطا در ارسال پیام: {str(e)}")
            return False
