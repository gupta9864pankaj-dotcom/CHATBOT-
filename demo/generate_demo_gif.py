from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
BG_TOP = (98, 148, 255)
BG_BOTTOM = (121, 84, 247)
WHITE = (255, 255, 255)
TEXT = (24, 25, 38)
BUBBLE_USER = (20, 122, 255)
BUBBLE_BOT = (236, 238, 242)

font_title = ImageFont.load_default()
font_body = ImageFont.load_default()

def gradient_bg():
    img = Image.new("RGB", (W, H), BG_TOP)
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        r = int(BG_TOP[0] * (1 - t) + BG_BOTTOM[0] * t)
        g = int(BG_TOP[1] * (1 - t) + BG_BOTTOM[1] * t)
        b = int(BG_TOP[2] * (1 - t) + BG_BOTTOM[2] * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    return img

def draw_card(draw, x1, y1, x2, y2, fill=(255, 255, 255, 230)):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=24, fill=fill)

def center_text(draw, text, y, fill=WHITE):
    bbox = draw.textbbox((0, 0), text, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y), text, font=font_title, fill=fill)

def slide_cover():
    img = gradient_bg()
    draw = ImageDraw.Draw(img, "RGBA")
    draw_card(draw, 210, 150, 1070, 560)
    center_text(draw, "QUOTES RECOMMENDATION CHATBOT", 220, fill=TEXT)
    center_text(draw, "Rasa + Flask | Emotion-aware | Multilingual", 280, fill=TEXT)
    center_text(draw, "Demo Video", 340, fill=TEXT)
    center_text(draw, "Motivation | Inspiration | Success | Love | Funny", 420, fill=TEXT)
    return img

def slide_setup():
    img = gradient_bg()
    draw = ImageDraw.Draw(img, "RGBA")
    draw_card(draw, 120, 80, 1160, 640)
    draw.text((170, 130), "Run Steps", font=font_title, fill=TEXT)
    lines = [
        "1) git clone <repo-url>",
        "2) conda create -n rasa_env python=3.10 -y",
        "3) conda activate rasa_env",
        "4) python -m pip install rasa -r requirements-web.txt",
        "5) python -m rasa train",
        "6) ./start_project.sh",
        "7) Open http://127.0.0.1:8010",
    ]
    y = 190
    for line in lines:
        draw.text((170, y), line, font=font_body, fill=TEXT)
        y += 60
    return img

def slide_chat_one():
    img = gradient_bg()
    draw = ImageDraw.Draw(img, "RGBA")
    draw_card(draw, 140, 70, 1140, 650)
    draw.text((180, 110), "Live Chat Demo", font=font_title, fill=TEXT)

    draw.rounded_rectangle([740, 180, 1070, 240], radius=18, fill=BUBBLE_USER)
    draw.text((770, 205), "i am stressed", font=font_body, fill=WHITE)

    draw.rounded_rectangle([190, 280, 940, 390], radius=18, fill=BUBBLE_BOT)
    draw.text((220, 305), "You are overloaded, not broken.", font=font_body, fill=TEXT)
    draw.text((220, 335), "Try 4 deep breaths + one 10-minute task.", font=font_body, fill=TEXT)

    draw.rounded_rectangle([740, 430, 1070, 490], radius=18, fill=BUBBLE_USER)
    draw.text((775, 455), "another quote", font=font_body, fill=WHITE)

    draw.rounded_rectangle([190, 535, 900, 610], radius=18, fill=BUBBLE_BOT)
    draw.text((220, 565), "Sure. Choose: motivation, inspiration, success...", font=font_body, fill=TEXT)
    return img

def slide_chat_two():
    img = gradient_bg()
    draw = ImageDraw.Draw(img, "RGBA")
    draw_card(draw, 140, 70, 1140, 650)
    draw.text((180, 110), "Multilingual Intent Demo", font=font_title, fill=TEXT)

    draw.rounded_rectangle([680, 190, 1070, 250], radius=18, fill=BUBBLE_USER)
    draw.text((710, 215), "mujhe motivation chahiye", font=font_body, fill=WHITE)

    draw.rounded_rectangle([190, 300, 900, 390], radius=18, fill=BUBBLE_BOT)
    draw.text((220, 325), "Motivation: Consistency beats intensity.", font=font_body, fill=TEXT)
    draw.text((220, 355), "Take one small step today.", font=font_body, fill=TEXT)

    draw.rounded_rectangle([760, 450, 1070, 510], radius=18, fill=BUBBLE_USER)
    draw.text((790, 475), "thank you", font=font_body, fill=WHITE)

    draw.rounded_rectangle([190, 560, 560, 620], radius=18, fill=BUBBLE_BOT)
    draw.text((220, 585), "You are welcome.", font=font_body, fill=TEXT)
    return img

def slide_end():
    img = gradient_bg()
    draw = ImageDraw.Draw(img, "RGBA")
    draw_card(draw, 200, 160, 1080, 540)
    center_text(draw, "Project Demo Completed", 250, fill=TEXT)
    center_text(draw, "Chatbot is ready for deployment", 320, fill=TEXT)
    center_text(draw, "Repository: gupta9864pankaj-dotcom/CHATBOT-", 390, fill=TEXT)
    return img

slides = [
    slide_cover(),
    slide_setup(),
    slide_chat_one(),
    slide_chat_two(),
    slide_end(),
]

frames = []
durations = []
for slide in slides:
    frames.append(slide)
    durations.append(2200)

frames[0].save(
    "demo/demo-video.gif",
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    optimize=False,
)
print("Created demo/demo-video.gif")
