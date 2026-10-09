"""Generate Jedag Jedug project directly for CapCut Desktop."""
import json
import os
import shutil
import sys
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from creative_mcp import capcut, templates

drafts_dir = capcut.drafts_dir()
target_name = "Jedag Jedug Beat Viral"
target_dir = drafts_dir / target_name

# Cache directories for generating source media
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
        draw.line([(0, y), (1080, y)], fill=(30, 35, 50))
    
    # Draw geometric glow card in center
    cx, cy = 540, 960
    cw, ch = 460, 600
    draw.rectangle([cx - cw, cy - ch, cx + cw, cy + ch], outline=col1, width=6)
    draw.rectangle([cx - cw + 20, cy - ch + 20, cx + cw - 20, cy + ch - 20], outline=(255, 255, 255, 120), width=2)
    
    # Draw text banners
    draw.text((cx, cy - 250), f"CAPCUT JJ #{i+1:02d}", fill=col1, anchor="mm", font_size=58)
    draw.text((cx, cy - 80), title, fill=(255, 255, 255), anchor="mm", font_size=74)
    draw.text((cx, cy + 90), sub, fill=col1, anchor="mm", font_size=42)
    draw.text((cx, cy + 280), "PREMIUM BEAT DROP SYNC", fill=(200, 200, 200), anchor="mm", font_size=32)
    
    out_file = images_dir / f"jj_photo_{i+1:02d}.jpg"
    img.save(out_file, quality=95)
    media_paths.append(str(out_file))

# 2. Prepare audio file
src_audio = audio_dir / "beat_music.wav"
if not src_audio.exists():
    src_audio = drafts_dir / "HUT49 Video1 SID" / "assets" / "audio" / "v1-music.wav"
dst_audio = audio_dir / "beat_music.wav"
if src_audio.exists() and src_audio != dst_audio:
    shutil.copy2(src_audio, dst_audio)
audio_path = str(dst_audio) if dst_audio.exists() else None

# 3. Build CapCut draft using base template with overwrite enabled
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
    base_draft="HUT49 Video1 SID" if (drafts_dir / "HUT49 Video1 SID").exists() else None,
    overwrite=True
)

# 4. Ensure assets directory in project is fully self-contained
assets_video = target_dir / "assets" / "video"
assets_audio = target_dir / "assets" / "audio"
assets_video.mkdir(parents=True, exist_ok=True)
assets_audio.mkdir(parents=True, exist_ok=True)

for i in range(1, 11):
    src_p = images_dir / f"jj_photo_{i:02d}.jpg"
    dst_p = assets_video / f"jj_photo_{i:02d}.jpg"
    if src_p.exists() and (not dst_p.exists() or dst_p.stat().st_size != src_p.stat().st_size):
        shutil.copy2(src_p, dst_p)

if dst_audio and dst_audio.exists():
    dst_proj_audio = assets_audio / "beat_music.wav"
    if not dst_proj_audio.exists() or dst_proj_audio.stat().st_size != dst_audio.stat().st_size:
        shutil.copy2(dst_audio, dst_proj_audio)

# 5. Clean up draft_content.json text layers and normalize paths
content_path = target_dir / "draft_content.json"
with open(content_path, "r", encoding="utf-8") as f:
    d = json.load(f)

draft_id = d["id"]
now_us = int(time.time() * 1_000_000)

clean_texts = [
    "JEDAG JEDUG VIRAL", "DROP BASS BOOM", "ULTRA WHITE FLASH", "3D ROTATION BEAT",
    "DYNAMIC SPEED CUT", "PUNCH IMPACT ZOOM", "CINEMATIC CAMERA PUSH", "RETRO FILM ROLL GLITCH",
    "NEON FLOW WIPE", "MOTION BLUR BURST", "SMOOTH FADE OUT", "Dibuat di CapCut Pro Web & MCP"
]
colors = [
    [1.0, 0.85, 0.0], [1.0, 0.0, 0.33], [0.0, 0.95, 1.0], [1.0, 0.9, 0.4],
    [0.24, 0.84, 0.88], [1.0, 0.25, 0.42], [0.66, 0.93, 0.92], [0.5, 0.0, 1.0],
    [0.07, 0.6, 0.56], [1.0, 0.29, 0.17], [0.23, 0.11, 0.44], [0.0, 0.9, 1.0]
]

for idx, tm in enumerate(d["materials"].get("texts", [])):
    pt = clean_texts[idx % len(clean_texts)]
    col = colors[idx % len(colors)]
    font_sz = 16.0 if idx == 0 else 10.0
    clean_obj = {
        "styles": [{
            "range": [0, len(pt)],
            "size": font_sz,
            "bold": False,
            "italic": False,
            "underline": False,
            "fill": {"alpha": 1.0, "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": col}}}
        }],
        "text": pt
    }
    tm["content"] = json.dumps(clean_obj, ensure_ascii=False)
    tm["check_flag"] = 7
    tm["typesetting"] = 0
    tm["alignment"] = 1

# Normalize video and audio material paths and build draft_materials metadata
meta_materials = []
for i, vm in enumerate(d["materials"].get("videos", [])):
    p = assets_video / f"jj_photo_{i+1:02d}.jpg"
    abs_p = str(p).replace("/", "\\")
    local_id = vm.get("local_material_id") or vm["id"]
    vm["path"] = abs_p
    vm["material_name"] = p.name
    vm["local_material_id"] = local_id
    vm["type"] = "photo"
    vm["width"] = 1080
    vm["height"] = 1920
    meta_materials.append({
        "ai_group_type": "",
        "create_time": -1,
        "duration": 10800000000,
        "enter_from": 0,
        "extra_info": p.name,
        "file_Path": f"./assets/video/{p.name}",
        "height": 1920,
        "id": local_id,
        "import_time": -1,
        "import_time_ms": -1,
        "item_source": 1,
        "material_color_tag": "",
        "md5": "",
        "metetype": "photo",
        "roughcut_time_range": {"duration": -1, "start": -1},
        "sub_time_range": {"duration": -1, "start": -1},
        "type": 0,
        "width": 1080
    })

if d["materials"].get("audios"):
    am = d["materials"]["audios"][0]
    p_audio = assets_audio / "beat_music.wav"
    abs_audio = str(p_audio).replace("/", "\\")
    audio_local_id = am.get("local_material_id") or am["id"]
    am["path"] = abs_audio
    am["name"] = p_audio.name
    am["type"] = "local_music"
    am["category_name"] = "local"
    am["local_material_id"] = audio_local_id
    meta_materials.append({
        "ai_group_type": "",
        "create_time": -1,
        "duration": am.get("duration", 10800000000),
        "enter_from": 0,
        "extra_info": p_audio.name,
        "file_Path": f"./assets/audio/{p_audio.name}",
        "height": 0,
        "id": audio_local_id,
        "import_time": -1,
        "import_time_ms": -1,
        "item_source": 1,
        "material_color_tag": "",
        "md5": "",
        "metetype": "music",
        "roughcut_time_range": {"duration": -1, "start": -1},
        "sub_time_range": {"duration": -1, "start": -1},
        "type": 0,
        "width": 0
    })

# Save updated draft_content.json
raw_content = json.dumps(d, ensure_ascii=False, indent=2).encode("utf-8")
content_path.write_bytes(raw_content)

# Update draft_info.json
info_data = {
    "id": draft_id,
    "name": target_name,
    "duration": d.get("duration", 0),
    "fps": d.get("fps", 30),
    "canvas_config": d.get("canvas_config", {}),
    "platform": {
        "app_source": "cc",
        "app_version": "9.5.0",
        "os": "windows"
    },
    "tracks": d.get("tracks", []),
    "materials": d.get("materials", {}),
    "extra_info": d.get("extra_info") or {}
}
(target_dir / "draft_info.json").write_bytes(json.dumps(info_data, ensure_ascii=False, indent=2).encode("utf-8"))

# Update template-2.tmp and Timelines
(target_dir / "template-2.tmp").write_bytes(raw_content)
tl_dir = target_dir / "Timelines"
tl_dir.mkdir(parents=True, exist_ok=True)

# Remove any stale timelines
for sub in tl_dir.iterdir():
    if sub.is_dir() and sub.name != draft_id:
        shutil.rmtree(sub, ignore_errors=True)

proj_json = {
    "config": {
        "color_space": -1,
        "hdr_vivid": False,
        "mixed_track_mode_on": False,
        "render_index_track_mode_on": False,
        "use_float_render": False
    },
    "create_time": now_us,
    "id": draft_id,
    "main_timeline_id": draft_id,
    "timelines": [
        {
            "create_time": now_us,
            "id": draft_id,
            "is_marked_delete": False,
            "name": "Timeline 01",
            "update_time": now_us
        }
    ],
    "update_time": now_us,
    "version": 0
}
(tl_dir / "project.json").write_bytes(json.dumps(proj_json, ensure_ascii=False, indent=2).encode("utf-8"))

tl_sub = tl_dir / draft_id
tl_sub.mkdir(parents=True, exist_ok=True)
(tl_sub / "draft_content.json").write_bytes(raw_content)
(tl_sub / "template-2.tmp").write_bytes(raw_content)

# Update draft_meta_info.json
meta_path = target_dir / "draft_meta_info.json"
meta_data = {}
if meta_path.exists():
    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            meta_data = json.load(f)
    except Exception:
        pass

meta_data["draft_id"] = draft_id
meta_data["draft_name"] = target_name
meta_data["draft_root_path"] = drafts_dir.as_posix()
meta_data["draft_fold_path"] = target_dir.as_posix()
meta_data["draft_timeline_materials_size_"] = len(raw_content)
meta_data["tm_duration"] = d.get("duration", 0)
meta_data["tm_draft_modified"] = now_us
meta_data["draft_materials"] = [{"type": 0, "value": meta_materials}]
meta_path.write_bytes(json.dumps(meta_data, ensure_ascii=False, indent=2).encode("utf-8"))

# 6. Generate cover image draft_cover.jpg (1280x720) in project directory
cover_img = Image.new("RGB", (1280, 720), "#0A0814")
c_draw = ImageDraw.Draw(cover_img)
for y in range(720):
    c_draw.line([(0, y), (1280, y)], fill=(int(10 + y * 0.02), int(8 + y * 0.01), int(20 + y * 0.05)))
c_draw.rectangle([60, 60, 1220, 660], outline="#FF0055", width=4)
c_draw.text((640, 280), "JEDAG JEDUG VIRAL", fill="#FFE66D", anchor="mm", font_size=84)
c_draw.text((640, 400), "10 TRANSISI · BEAT DROP PULSE · CAPCUT PRO", fill="#FFFFFF", anchor="mm", font_size=36)
c_draw.text((640, 490), "TERHUBUNG 100% KE CAPCUT DESKTOP", fill="#3DD6E0", anchor="mm", font_size=28)
cover_path = target_dir / "draft_cover.jpg"
cover_img.save(cover_path, quality=95)

# 7. Ensure root meta is synced
capcut.sync_root_meta(target_name, int(d.get("duration", 8.0) * 1_000_000))

print("SUCCESS: Jedag Jedug draft built!")
print("Project path:", str(target_dir))
print("Cover path:", str(cover_path))
print("Duration:", d.get("duration"), "seconds")
print(f"Materials linked: {len(meta_materials)} ({len(d['materials'].get('videos', []))} photos + {len(d['materials'].get('audios', []))} audios)")
