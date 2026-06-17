from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.request
from PIL import Image, ImageDraw, ImageFont
import io

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Разбираем никнейм из ссылки (?nick=...)
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        nick = query_params.get('nick', ['Sky'])[0]
        
        text = f"Nickname {nick} is registered."
        
        # Размеры плашки (стандартный форумный юзербар)
        width = 450
        height = 35
        
        # 2. Создаем пустой холст
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # 3. ГЕНЕРИРУЕМ КРАСИВЫЙ ГРАДИЕНТ (Чистый код вместо bg.png)
        # Цвета перехода: от глубокого черного к стильному сине-стальному (как на твоем скрине)
        color_start = (5, 17, 29)     # Темный левый край #05111d
        color_end = (40, 90, 125)     # Синеватый правый край #285a7d
        
        for x in range(width):
            # Вычисляем промежуточный цвет для каждого пикселя по горизонтали
            r = int(color_start[0] + (color_end[0] - color_start[0]) * (x / width))
            g = int(color_start[1] + (color_end[1] - color_start[1]) * (x / width))
            b = int(color_start[2] + (color_end[2] - color_start[2]) * (x / width))
            draw.line([(x, 0), (x, height)], fill=(r, g, b))
            
        # 4. ДОБАВЛЯЕМ ДЕТАЛИ ОФОРМЛЕНИЯ
        # Тонкая внутренняя рамка для эффекта стекла/объема
        draw.rectangle([0, 0, width - 1, height - 1], outline=(60, 120, 160)) # Слегка светящаяся рамка
        
        # Небольшая декоративная точка-индикатор (как статус "онлайн")
        draw.ellipse([15, 13, 21, 19], fill=(0, 255, 150)) # Ярко-зеленый маркер
        
        # 5. ДИНАМИЧЕСКИЙ ШРИФТ ИЗ СЕТИ (Вместо font.ttf)
        # Скачиваем аккуратный пиксельный шрифт "Silkscreen" прямо во время работы
        font_url = "https://github.com/google/fonts/raw/main/ofl/silkscreen/Silkscreen-Regular.ttf"
        try:
            font_data = urllib.request.urlopen(font_url).read()
            font = ImageFont.truetype(io.BytesIO(font_data), 11) # 11 — идеальный размер для этого шрифта
        except Exception:
            font = ImageFont.load_default() # Резервный вариант, если интернеты упадут
            
        # 6. РИСУЕМ ТЕКСТ
        # Сдвигаем текст чуть правее зеленого маркера (X=32) и центрируем по вертикали (Y=10)
        draw.text((32, 10), text, fill=(255, 255, 255), font=font)
        
        # Правый водяной знак (опционально, можно стереть или написать свой сайт)
        draw.text((width - 110, 10), "XenForo Status", fill=(130, 180, 210), font=font)
        
        # 7. ОТДАЕМ КАРТИНКУ НА ФОРУМ
        byte_io = io.BytesIO()
        img.save(byte_io, 'PNG')
        byte_io.seek(0)
        
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.end_headers()
        self.wfile.write(byte_io.getvalue())
        return
