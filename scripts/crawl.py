import wikipediaapi
import os
import json
import re

class WikipediaPage:
    TOPICS = ['Lịch sử Việt Nam','Việt Nam thời tiền sử','Bắc thuộc','Hùng Vương','Văn Lang','An Dương Vương','Âu Lạc',
          'Thời kỳ Bắc thuộc lần thứ nhất','Thời kỳ Bắc thuộc lần thứ hai','Thời kỳ tự chủ Việt Nam',
          'Thời kỳ Bắc thuộc lần thứ ba','Thời kỳ Bắc thuộc lần thứ tư','Nhà Ngô','Loạn 12 sứ quân',
          'Nhà Đinh','Nhà Tiền Lê','Nhà Lý','Nhà Trần','Nhà Hồ','Nhà Hậu Lê','Nhà Mạc',
          'Chiến tranh Lê – Mạc','Trịnh – Nguyễn phân tranh','Nhà Tây Sơn','Nhà Nguyễn',
          'Pháp thuộc','Biên niên sử Việt Nam thời kỳ 1945–1975']
    
    def __init__(self, language='vi', user_agent='rag (pqtrung34@gmail.com)', ):
        self.topics = self.TOPICS
        self.language = language
        self.user_agent = user_agent
        self.wiki = wikipediaapi.Wikipedia(user_agent='rag (pqtrung34@gmail.com)', 
                              language='vi',
                              extract_format=wikipediaapi.ExtractFormat.WIKI)
        self.pages = {}

    @staticmethod
    def clean_text(text):
        """Xử lý văn bản Wikipedia để làm sạch định dạng"""
        # Loại bỏ định dạng in đậm/in nghiêng wiki: '''...''' hoặc ''...''
        text = re.sub(r"''+([^']+)''+", r"\1", text)

        # Loại bỏ liên kết nội bộ [[...]]
        text = re.sub(r'\[\[([^|\]]+\|)?([^\]]+)\]\]', r'\2', text)

        # Loại bỏ các tiêu đề wiki == Tiêu đề ==
        text = re.sub(r'^=+\s*(.*?)\s*=+$', r'\1', text, flags=re.MULTILINE)

        # Xoá các chú thích kiểu [1], [2], ...
        text = re.sub(r'\[\d+\]', '', text)

        # Xoá dòng trắng dư thừa
        text = re.sub(r'\n{2,}', '\n\n', text)

        # Loại bỏ khoảng trắng đầu/cuối
        text = text.strip()

        return text
        
    def get_page(self, topic):
        # Lấy nội dung 1 chủ để
        page = self.wiki.page(topic)
        if page.exists():
            return self.clean_text(page.text)
        else:
            return None
        
    def get_all_pages(self, filename):
        # Lấy nội dung toàn bộ chủ đề
        for topic in self.topics:
            content = self.get_page(topic)
            if content:
                self.pages[topic] = content

        # Lưu vào file
        self.save(filename)

    def save(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            for topic, content in self.pages.items():
                f.write(f"=== {topic} ===\n")
                f.write(content)
                f.write("\n\n")