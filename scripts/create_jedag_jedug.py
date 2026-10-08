"""Generate Jedag Jedug project directly for CapCut Desktop."""
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from creative_mcp import capcut, templates

drafts_dir = capcut.drafts_dir()
target_name = "Jedag Jedug Beat Viral"
target_dir = drafts_dir / target_name

# Delete old test directory if exists
if target_dir.exists():
    import shutil
    shutil.rmtree(target_dir, ignore_errors=True)

# Temporary media directory
media_cache_dir = drafts_dir / "_cache_media"
images_dir = media_cache_dir / "images"
audio_dir = media_cache_dir / "audio"
images_dir.mkdir(parents=True, exist_ok=True)
audio_dir.mkdir(parents=True, exist_ok=True)

# 1. Generate 10 high-resolution edited photos (1080x1920)
photo_themes = [
    ("BEAT 01: GLITCH", "#FF0055", "#18002E", "DROP BASS BOOM"),
    ("BEAT 02: FLASH", "#00F2FE", "#001233", "ULTRA WHITE FLASH"),
    ("BEAT 03: SPIN", "#FFE66D", "#33001B", "3D ROTATION BEAT"),
    ("BEAT 04: SLIDE", "#3DD6E0", "#0B132B", "DYNAMIC SPEED CUT"),
    ("BEAT 05: ZOOM", "#FF416C", "#1F0429", "PUNCH IMPACT ZOOM"),
    ("BEAT 06: PUSH", "#A8EDEA", "#1A1A24", "CINEMATIC CAMERA PUSH"),
    ("BEAT 07: ROLL", "#7F00FF", "#0C071E", "RETRO FILM ROLL GLITCH"),
    ("BEAT 08: WIPE", "#11998E", "#061A14", "NEON FLOW WIPE"),
    ("BEAT 09: BLUR", "#FF4B2B", "#2B0B00", "MOTION BLUR BURST"),
    ("BEAT 10: FADE", "#3A1C71", "#05050A", "SMOOTH FADE OUT")
]

media_paths = []
for i, (title, col1, col2, sub) in enumerate(photo_themes):
    img = Image.new("RGB", (1080, 1920), col2)
    draw = ImageDraw.Draw(img)
    
    # Draw background gradient bars and tech grid
    for y in range(0, 1920, 40):
        alpha = int(255 * (y / 1920.0))
        # subtle lines
        draw.line([(0, y), (1080, y)], fill=(30, 35, 50))
    
    # Draw geometric glow card in center
    cx, cy = 540, 960
    cw, ch = 460, 600
    draw.rectangle([cx - cw, cy - ch, cx + cw, cy + ch], outline=col1, width=6)
    
    # Internal accent accents
    draw.rectangle([cx - cw + 20, cy - ch + 20, cx + cw - 20, cy + ch - 20], outline=(255, 255, 255, 120), width=2)
    
    # Draw text banners
    draw.text((cx, cy - 250), f"CAPCUT JJ #{i+1:02d}", fill=col1, anchor="mm", font_size=58)
    draw.text((cx, cy - 80), title, fill=(255, 255, 255), anchor="mm", font_size=74)
    draw.text((cx, cy + 90), sub, fill=col1, anchor="mm", font_size=42)
    draw.text((cx, cy + 280), "PREMIUM BEAT DROP SYNC", fill=(200, 200, 200), anchor="mm", font_size=32)
    
    out_file = images_dir / f"jj_photo_{i+1:02d}.jpg"
    img.save(out_file, quality=95)
    media_paths.append(str(out_file))

# 2. Audio file
src_audio = drafts_dir / "HUT49 Video1 SID" / "assets" / "audio" / "v1-music.wav"
dst_audio = audio_dir / "beat_music.wav"
if src_audio.exists():
    import shutil
    shutil.copy2(src_audio, dst_audio)
    audio_path = str(dst_audio)
else:
    audio_path = None

# 3. Build CapCut draft using base template
captions = [p[3] for p in photo_themes]
res = templates.build_capcut(
    template="jedagjedug",
    name=target_name,
    media=media_paths,
    title="JEDAG JEDUG VIRAL",
    captions=captions,
    cta="Dibuat di CapCut Pro Web & MCP",
    music=audio_path,
    palette="neon",
    clip_seconds=0.75,
    base_draft="HUT49 Video1 SID" if (drafts_dir / "HUT49 Video1 SID").exists() else None
)

# 4. Generate cover image draft_cover.jpg (1280x720) in project directory
cover_img = Image.new("RGB", (1280, 720), "#0A0814")
c_draw = ImageDraw.Draw(cover_img)
for y in range(720):
    c_draw.line([(0, y), (1280, y)], fill=(int(10 + y * 0.02), int(8 + y * 0.01), int(20 + y * 0.05)))
c_draw.rectangle([60, 60, 1220, 660], outline="#FF0055", width=4)
c_draw.text((640, 280), "JEDAG JEDUG VIRAL", fill="#FFE66D", anchor="mm", font_size=84)
c_draw.text((640, 400), "10 TRANSISI \u00b7 BEAT DROP PULSE \u00b7 CAPCUT PRO", fill="#FFFFFF", anchor="mm", font_size=36)
c_draw.text((640, 490), "TERHUBUNG 100% KE CAPCUT DESKTOP", fill="#3DD6E0", anchor="mm", font_size=28)
cover_path = target_dir / "draft_cover.jpg"
cover_img.save(cover_path, quality=95)

# 5. Ensure cover is properly saved and sync root meta
capcut.sync_root_meta(target_name, int(res.get("duration", 8.0) * 1_000_000))

print("SUCCESS: Jedag Jedug draft built!")
print("Project path:", str(target_dir))
print("Cover path:", str(cover_path))
print("Duration:", res.get("duration"), "seconds")
print("Elements:", res.get("elements"))
