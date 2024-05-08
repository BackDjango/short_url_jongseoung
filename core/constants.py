import json


class SystemCodeManager:
    """
    ex)
    status_code, message_ko = SystemCodeManager.get_message("auth_code", "SUCCESS")
    status_code, message_en = SystemCodeManager.get_message("auth_code", "SUCCESS", 'en')
    """

    @classmethod
    def get_message(cls, system_code_type, message, lang="ko"):
        filepath = f"core/system_codes/{system_code_type}.json"
        messages = cls.load_messages(filepath)

        if message in messages:
            data = messages[message]
            if lang in data:
                return data["code"], data[lang]
        else:
            return SystemCodeManager.get_message("base_code", "SYSTEM_CODE_ERROR")
        return None

    @staticmethod
    def load_messages(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)["SYSTEM_CODE"]
