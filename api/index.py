from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from PIL import Image, ImageDraw, ImageFont
import io
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Разбираем параметры ссылки (ищем ?nick=...)
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        nick = query_params.get('nick', ['Guest'])[0]
        
        text = f"Nickname {nick} is registered."
        
        # Определяем пути к фону и шрифту (они лежат в корне репозитория)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(current_dir, '..', 'bg.png')
        font_path = os.path.join(current_dir, '..', 'font.ttf')
        
        # 2. Загружаем твой дизайн фона (или создаем пустой, если файла нет)
        if os.path.exists(bg_path):
            img = Image.open(bg_path)
        else:
            img = Image.new('RGB', (450, 32), color='#0d1b2a')
            
        draw = ImageDraw.Draw(img)
        
        # 3. Загружаем твой пиксельный шрифт
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, 16) # 16 — размер шрифта
        else:
            font = ImageFont.load_default()
            
        # 4. Рисуем текст белым цветом
        # (15, 6) — это координаты отступа слева и сверху. Подгони под свой фон!
        draw.text((15, 6), text, fill="#ffffff", font=font)
        
        # 5. Превращаем готовую картинку в байты
        byte_io = io.BytesIO()
        img.save(byte_io, 'PNG')
        byte_io.seek(0)
        
        # 6. Отправляем картинку в ответ на запрос XenForo
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        # Запрещаем жесткое кэширование, чтобы ники менялись мгновенно
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.end_headers()
        self.wfile.write(byte_io.getvalue())
        return
