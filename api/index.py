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
        nick = query_params.get('nick', ['sky'])[0]
        
        # Новый стиль текста: "Nah, I’m a [белый] {nick}.[малиновый]"
        base_text = "Nah, I’m a "
        # Добавим точку, как на картинке, для "sky."
        nick_text = f"{nick}."
        
        # Установим размер плашки
        width = 450
        height = 42
        
        # 2. Создаем холст с глубоким матовым премиум-цветом (Глубокий графит #0d0e12)
        img = Image.new('RGB', (width, height), color=(13, 14, 18))
        draw = ImageDraw.Draw(img)
        
        # 3. ВИЗУАЛЬНОЕ УЛУЧШЕНИЕ ПЛАШКИ

        # ЦВЕТА ИЗМЕНЕНЫ НА МАЛИНОВЫЙ/РОЗОВЫЙ (на основе image_2.png)
        # Малиновый неон `#ff006e` (255, 0, 110)
        # Белый матовый `#f3f4f6` (243, 244, 246)
        color_neon = (255, 0, 110)
        color_text_white = (243, 244, 246)

        # Сделать рамку закругленной! (Пользователь просил "не просто")
        # radius - радиус закругления. `width` - толщина. `outline` - цвет.
        # Попробуем использовать rounded_rectangle. На новых версиях Pillow он доступен.
        try:
            draw.rounded_rectangle([0, 0, width - 1, height - 1], radius=8, outline=(31, 33, 42), width=1)
        except AttributeError:
            # Резервный вариант для старых Pillow, если ошибка:
            draw.rectangle([0, 0, width - 1, height - 1], outline=(31, 33, 42), width=1)
        
        # Свежий акцент: Тонкая малиновая неоновая линия слева (заменили фиолетовую)
        # Оставим яркую линию, она выглядит стильно и неоново
        draw.line([2, 5, 2, height - 6], fill=color_neon, width=2)
        
        # ДОБАВЛЕНИЕ ЭЛЕМЕНТОВ (Звездочки/частицы)
        # Нарисуем несколько декоративных, разного размера неоновых кругов в левой части
        # имитация неоновых "звездочек" или "частиц"
        # координаты (x, y, x+radius, y+radius)
        # Частица 1: Большая малиновая
        draw.ellipse([14, 11, 20, 17], fill=color_neon)
        # Частица 2: Средняя белая
        draw.ellipse([12, 19, 16, 23], fill=color_text_white)
        # Частица 3: Маленькая малиновая
        draw.ellipse([18, 16, 21, 19], fill=color_neon)

        # 4. ШРИФТ ИЗ СЕТИ
        # Скачиваем Inter-SemiBold. Он жирнее, чем Medium, чтобы быть ближе к «sky.», но аккуратный.
        font_url = "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/static/Inter-SemiBold.ttf"
        try:
            req = urllib.request.Request(
                font_url, 
                headers={'User-Agent': 'Mozilla/5.0'} 
            )
            font_data = urllib.request.urlopen(req).read()
            font = ImageFont.truetype(io.BytesIO(font_data), 14) # Размер 14
        except Exception:
            font = ImageFont.load_default()
            
        # 5. СЛОЖНЫЙ РЕНДЕРИНГ ТЕКСТА (СМЕШАННЫЕ ЦВЕТА КАК НА КАРТИНКЕ)
        # anchor="lm" выравнивает по центру вертикали. 
        # Отступ слева 32 пикселя (после частиц).
        x_pos = 32
        y_pos = height / 2

        # Нарисовать первую часть белым
        draw.text((x_pos, y_pos), base_text, fill=color_text_white, font=font, anchor="lm")
        
        # Вычислить длину первой части, чтобы узнать, где рисовать ник
        first_part_len = font.getlength(base_text)
        
        # Нарисовать ник малиновым с правильным отступом
        draw.text((x_pos + first_part_len, y_pos), nick_text, fill=color_neon, font=font, anchor="lm")
        
        # 6. ОТПРАВЛЯЕМ КАРТИНКУ НА ФОРУМ
        byte_io = io.BytesIO()
        img.save(byte_io, 'PNG')
        byte_io.seek(0)
        
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.end_headers()
        self.wfile.write(byte_io.getvalue())
        return