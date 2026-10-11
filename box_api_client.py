from openai import OpenAI
from config import BOXAPI_API_KEY, BOXAPI_BASE_URL, BOXAPI_MODEL, SYSTEM_PROMPT


class BoxAPIClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=BOXAPI_API_KEY,
            base_url=BOXAPI_BASE_URL,
        )
        self.model = BOXAPI_MODEL
        self.system_prompt = SYSTEM_PROMPT

    def send_message_with_context(self, user_message, recent_messages=[]):
        """
        ارسال پیام کاربر با context پیام‌های قبلی به BoxAPI
        """
        messages = [{"role": "system", "content": self.system_prompt}]

        if recent_messages:
            messages += recent_messages[-10:]  # فقط ۱۰ پیام آخر
            print(f"📚 Context شامل {len(recent_messages)} پیام قبلی")

        messages.append({"role": "user", "content": user_message})
        return self._send_to_api(messages, user_message)

    def send_message(self, user_message):
        """
        ارسال پیام بدون context
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message},
        ]
        return self._send_to_api(messages, user_message)

    def _send_to_api(self, messages, user_message):
        """
        ارسال پیام‌ها به BoxAPI و برگرداندن پاسخ
        """
        try:
            print(f"🤖 در حال ارسال پیام به BoxAPI: {user_message[:50]}...")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )

            ai_response = response.choices[0].message.content
            print(f"✅ پاسخ از BoxAPI دریافت شد: {ai_response[:50]}...")
            return ai_response

        except Exception as e:
            print(f"❌ خطا در ارتباط با BoxAPI: {str(e)}")
            return "متاسفانه الان نمی‌تونم جواب بدم 😢 اینترنت یا سرور مشکل داره!"

    def test_connection(self):
        """
        تست اتصال به BoxAPI
        """
        try:
            response = self.send_message("سلام! این یک تست است.")
            if response and "خطا" not in response and "مشکل" not in response:
                print("✅ اتصال به BoxAPI موفقیت‌آمیز است")
                return True
            else:
                print("❌ مشکل در اتصال به BoxAPI")
                return False
        except Exception as e:
            print(f"❌ خطا در تست اتصال: {str(e)}")
            return False
