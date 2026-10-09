"""Generate ultra-high aesthetic Jedag Jedug project directly for CapCut Desktop."""
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

# 10 High-res aesthetic generated AI images
artifact_dir = Path(r"C:\Users\arche\.gemini\antigravity-ide\brain\7b33cbb1-5f5c-409c-a87e-055fe7311b58")

source_images = [
    artifact_dir / "jj_cyberpunk_hero_1791524713692.jpg",
    artifact_dir / "jj_supercar_neon_1791524733513.jpg",
    artifact_dir / "jj_festival_dj_1791524777892.jpg",
    artifact_dir / "jj_cyber_fashion_1791524807021.jpg",
    artifact_dir / "jj_cyber_bike_1791524831174.jpg",
    artifact_dir / "jj_neon_katana_1791525052107.jpg",
    artifact_dir / "jj_cockpit_pov_1791525075308.jpg",
    artifact_dir / "jj_neon_dancer_1791525099535.jpg",
    artifact_dir / "jj_tokyo_cross_1791525118990.jpg",
    artifact_dir / "jj_studio_beats_1791525140462.jpg",
]

captions = [
    "CYBERPUNK BEAT",
    "HYPER DRIFT",
    "BASS IMPACT",
    "HOLO GLOW",
    "TURBO RUSH",
    "NEON SLASH",
    "HYPER SPEED",
    "ENERGY FLOW",
    "NEON METROPOLIS",
    "SOUND WAVE"
]

media_paths = []
for i, src in enumerate(source_images):
    out_file = images_dir / f"jj_photo_{i+1:02d}.jpg"
    if src.exists():
        shutil.copy2(src, out_file)
    media_paths.append(str(out_file))

# Audio file preparation (local free music)
src_audio = audio_dir / "beat_music.wav"
if not src_audio.exists():
    src_audio = drafts_dir / "HUT49 Video1 SID" / "assets" / "audio" / "v1-music.wav"
dst_audio = audio_dir / "beat_music.wav"
if src_audio.exists() and src_audio != dst_audio:
    shutil.copy2(src_audio, dst_audio)
audio_path = str(dst_audio) if dst_audio.exists() else None

# Build CapCut draft using jedagjedug template
res = templates.build_capcut(
    template="jedagjedug",
    name=target_name,
    media=media_paths,
    title="JEDAG JEDUG VIRAL",
    captions=captions,
    cta="",
    music=audio_path,
    palette="neon",
    clip_seconds=0.75,
    base_draft="HUT49 Video1 SID" if (drafts_dir / "HUT49 Video1 SID").exists() else None,
    overwrite=True
)

# Ensure project asset dirs exist
assets_video = target_dir / "assets" / "video"
assets_audio = target_dir / "assets" / "audio"
assets_video.mkdir(parents=True, exist_ok=True)
assets_audio.mkdir(parents=True, exist_ok=True)

for i in range(1, 11):
    src_p = images_dir / f"jj_photo_{i:02d}.jpg"
    dst_p = assets_video / f"jj_photo_{i:02d}.jpg"
    if src_p.exists():
        shutil.copy2(src_p, dst_p)

if dst_audio and dst_audio.exists():
    dst_proj_audio = assets_audio / "beat_music.wav"
    shutil.copy2(dst_audio, dst_proj_audio)

# Load generated draft_content.json and polish texts
content_path = target_dir / "draft_content.json"
with open(content_path, "r", encoding="utf-8") as f:
    d = json.load(f)

draft_id = d["id"]
now_us = int(time.time() * 1_000_000)

clean_texts = ["JEDAG JEDUG VIRAL"] + captions
text_colors = [
    [1.0, 0.9, 0.0],   # Yellow gold
    [0.0, 0.95, 1.0],  # Cyan
    [1.0, 0.0, 0.4],   # Neon pink
    [0.0, 1.0, 0.55],  # Neon green
    [0.6, 0.2, 1.0],   # Purple
    [1.0, 0.5, 0.0],   # Orange
    [0.0, 0.8, 1.0],   # Electric blue
    [1.0, 0.1, 0.6],   # Magenta
    [0.4, 1.0, 0.8],   # Mint
    [1.0, 0.85, 0.2],  # Warm gold
    [0.7, 0.3, 1.0]    # Violet
]

for idx, tm in enumerate(d["materials"].get("texts", [])):
    pt = clean_texts[idx % len(clean_texts)]
    col = text_colors[idx % len(text_colors)]
    font_sz = 15.0 if idx == 0 else 10.0
    clean_obj = {
        "styles": [{
            "range": [0, len(pt)],
            "size": font_sz,
            "bold": True,
            "italic": False,
            "underline": False,
            "fill": {"alpha": 1.0, "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": col}}}
        }],
        "text": pt
    }
    tm["content"] = json.dumps(clean_obj, separators=(",", ":"), ensure_ascii=False)
    tm["check_flag"] = 7
    tm["typesetting"] = 0
    tm["alignment"] = 1
    tm["text_color"] = "#FFE500" if idx == 0 else "#00F2FE"
    tm["font_size"] = font_sz

# Video and audio material metadata
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

raw_content = json.dumps(d, ensure_ascii=False, indent=2).encode("utf-8")

# 1. Write root draft files
content_path.write_bytes(raw_content)
(target_dir / "template-2.tmp").write_bytes(raw_content)

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

# 2. Write Timelines and project.json (supporting active open timelines)
tl_dir = target_dir / "Timelines"
tl_dir.mkdir(parents=True, exist_ok=True)

# Detect if CapCut has an existing timeline registered
existing_tl_id = None
tl_proj_file = tl_dir / "project.json"
if tl_proj_file.exists():
    try:
        t_data = json.loads(tl_proj_file.read_text("utf-8"))
        existing_tl_id = t_data.get("main_timeline_id") or t_data.get("id")
    except Exception:
        pass

timeline_ids_to_update = {draft_id}
if existing_tl_id:
    timeline_ids_to_update.add(existing_tl_id)

proj_json = {
    "config": {
        "color_space": -1,
        "hdr_vivid": False,
        "mixed_track_mode_on": False,
        "render_index_track_mode_on": False,
        "use_float_render": False
    },
    "create_time": now_us,
    "id": existing_tl_id or draft_id,
    "main_timeline_id": existing_tl_id or draft_id,
    "timelines": [
        {
            "create_time": now_us,
            "id": existing_tl_id or draft_id,
            "is_marked_delete": False,
            "name": "Timeline 01",
            "update_time": now_us
        }
    ],
    "update_time": now_us,
    "version": 0
}
tl_proj_file.write_bytes(json.dumps(proj_json, ensure_ascii=False, indent=2).encode("utf-8"))

for tid in timeline_ids_to_update:
    tl_sub = tl_dir / tid
    tl_sub.mkdir(parents=True, exist_ok=True)
    # Also adjust draft id inside draft_content if targeting existing_tl_id
    d_clone = dict(d)
    d_clone["id"] = tid
    tl_content = json.dumps(d_clone, ensure_ascii=False, indent=2).encode("utf-8")
    (tl_sub / "draft_content.json").write_bytes(tl_content)
    (tl_sub / "template-2.tmp").write_bytes(tl_content)

# 3. Create high-aesthetic cover draft_cover.jpg
cover_src = source_images[1] if source_images[1].exists() else source_images[0]
with Image.open(cover_src) as img_in:
    # Resize and crop to 1280x720 landscape banner
    target_aspect = 1280 / 720
    orig_w, orig_h = img_in.size
    crop_h = int(orig_w / target_aspect)
    crop_top = (orig_h - crop_h) // 2
    cropped = img_in.crop((0, crop_top, orig_w, crop_top + crop_h))
    cover_img = cropped.resize((1280, 720), Image.Resampling.LANCZOS)

c_draw = ImageDraw.Draw(cover_img)
# Dark vignette gradient overlay for text readability
for y in range(500, 720):
    alpha = int((y - 500) / 220 * 200)
    c_draw.line([(0, y), (1280, y)], fill=(0, 0, 0))

c_draw.text((640, 560), "JEDAG JEDUG VIRAL", fill="#FFE500", anchor="mm", font_size=68)
c_draw.text((640, 630), "CYBERPUNK BEAT DROP · 10 TRANSITIONS · 4K", fill="#00F2FE", anchor="mm", font_size=30)

cover_path = target_dir / "draft_cover.jpg"
cover_img.save(cover_path, quality=95)
for tid in timeline_ids_to_update:
    (tl_dir / tid / "draft_cover.jpg").write_bytes(cover_path.read_bytes())

# 4. Update draft_meta_info.json
meta_path = target_dir / "draft_meta_info.json"
meta_data = {}
if meta_path.exists():
    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            meta_data = json.load(f)
    except Exception:
        pass

meta_data["draft_id"] = existing_tl_id or draft_id
meta_data["draft_name"] = target_name
meta_data["draft_root_path"] = drafts_dir.as_posix()
meta_data["draft_fold_path"] = target_dir.as_posix()
meta_data["draft_timeline_materials_size_"] = len(raw_content)
meta_data["tm_duration"] = d.get("duration", 0)
meta_data["tm_draft_modified"] = now_us
meta_data["draft_materials"] = [{"type": 0, "value": meta_materials}]
meta_path.write_bytes(json.dumps(meta_data, ensure_ascii=False, indent=2).encode("utf-8"))

# 5. Register in root_meta_info.json
capcut.sync_root_meta(target_name, int(d.get("duration", 7.5) * 1_000_000))

print("SUCCESS: Ultra-aesthetic Jedag Jedug draft successfully generated and synchronized!")
print("Project path:", str(target_dir))
print("Cover path:", str(cover_path))
print("Duration:", d.get("duration"), "seconds")
print(f"Materials linked: {len(meta_materials)} ({len(d['materials'].get('videos', []))} photos + {len(d['materials'].get('audios', []))} audios)")
