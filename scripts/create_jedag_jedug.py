"""Generate ultra-high aesthetic Jedag Jedug project directly for CapCut Desktop.
Uses 10 photorealistic cyberpunk visual assets, beat-synced scale keyframes,
clean solid-fill subtitles, and synchronizes timeline structures with root_meta_info.json.
"""
import json
import os
import shutil
import sys
import time
import uuid
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from creative_mcp import capcut

drafts_dir = capcut.drafts_dir()
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


def make_premium_cover(src_path: Path, out_path: Path):
    """Generate high-end 1280x720 landscape cover thumbnail."""
    with Image.open(src_path) as im:
        target_ratio = 1280 / 720
        w, h = im.size
        crop_h = int(w / target_ratio)
        top = (h - crop_h) // 2
        cropped = im.crop((0, top, w, top + crop_h))
        cover = cropped.resize((1280, 720), Image.Resampling.LANCZOS)

    draw = ImageDraw.Draw(cover)
    for y in range(480, 720):
        draw.line([(0, y), (1280, y)], fill=(10, 12, 18))

    draw.text((640, 560), "JEDAG JEDUG VIRAL", fill="#FFE500", anchor="mm", font_size=64)
    draw.text((640, 630), "CYBERPUNK BEAT DROP · 10 TRANSISI · 4K 60FPS", fill="#00F2FE", anchor="mm", font_size=28)
    cover.save(out_path, quality=95)


def sync_project(project_name: str, project_id: str):
    """Synchronize a single CapCut project completely with clean timeline architecture."""
    proj_dir = drafts_dir / project_name
    proj_dir.mkdir(parents=True, exist_ok=True)

    v_dir = proj_dir / "assets" / "video"
    a_dir = proj_dir / "assets" / "audio"
    v_dir.mkdir(parents=True, exist_ok=True)
    a_dir.mkdir(parents=True, exist_ok=True)

    for i, src in enumerate(source_images):
        dst = v_dir / f"jj_photo_{i+1:02d}.jpg"
        if src.exists():
            shutil.copy2(src, dst)

    src_audio = drafts_dir / "HUT49 Video1 SID" / "assets" / "audio" / "v1-music.wav"
    dst_audio = a_dir / "beat_music.wav"
    if src_audio.exists() and not dst_audio.exists():
        shutil.copy2(src_audio, dst_audio)

    cover_file = proj_dir / "draft_cover.jpg"
    make_premium_cover(source_images[1], cover_file)

    tl_dir = proj_dir / "Timelines"
    tl_dir.mkdir(parents=True, exist_ok=True)
    for sub in tl_dir.iterdir():
        if sub.is_dir() and sub.name != project_id:
            shutil.rmtree(sub, ignore_errors=True)

    now_us = int(time.time() * 1_000_000)
    beat_dur = 750000
    num_clips = len(source_images)
    total_duration_us = num_clips * beat_dur

    captions = [
        "CYBERPUNK BEAT", "HYPER DRIFT", "BASS IMPACT", "HOLO GLOW", "TURBO RUSH",
        "NEON SLASH", "HYPER SPEED", "ENERGY FLOW", "NEON METROPOLIS", "SOUND WAVE"
    ]

    track_video_id = str(uuid.uuid4()).lower()
    track_text_id = str(uuid.uuid4()).lower()
    track_audio_id = str(uuid.uuid4()).lower()

    tracks = [
        {"id": track_video_id, "type": "video", "segments": [], "attribute": 0, "flag": 0},
        {"id": track_text_id, "type": "text", "segments": [], "attribute": 0, "flag": 0},
        {"id": track_audio_id, "type": "audio", "segments": [], "attribute": 0, "flag": 0}
    ]

    materials_videos = []
    materials_texts = []
    materials_speeds = []
    materials_audios = []
    meta_materials = []

    for i in range(num_clips):
        vid_mat_id = str(uuid.uuid4()).lower()
        seg_id = str(uuid.uuid4()).lower()
        speed_id = str(uuid.uuid4()).lower()
        fname = f"jj_photo_{i+1:02d}.jpg"
        abs_p = str(v_dir / fname).replace("/", "\\")

        materials_videos.append({
            "id": vid_mat_id,
            "local_material_id": vid_mat_id,
            "type": "photo",
            "material_name": fname,
            "path": abs_p,
            "width": 1080,
            "height": 1920
        })

        meta_materials.append({
            "ai_group_type": "", "create_time": -1, "duration": 10800000000, "enter_from": 0,
            "extra_info": fname, "file_Path": f"./assets/video/{fname}", "height": 1920,
            "id": vid_mat_id, "import_time": -1, "import_time_ms": -1, "item_source": 1,
            "material_color_tag": "", "md5": "", "metetype": "photo",
            "roughcut_time_range": {"duration": -1, "start": -1},
            "sub_time_range": {"duration": -1, "start": -1}, "type": 0, "width": 1080
        })

        materials_speeds.append({
            "id": speed_id, "type": "speed", "mode": 0, "speed": 1.0, "curve_speed": None
        })

        is_even = (i % 2 == 0)
        kf_list = [
            {"curveType": "Line", "graphID": "", "id": str(uuid.uuid4()).lower(), "left_control": {"x": 0.0, "y": 0.0},
             "right_control": {"x": 0.0, "y": 0.0}, "time_offset": 0, "values": [1.05 if is_even else 1.25]},
            {"curveType": "Line", "graphID": "", "id": str(uuid.uuid4()).lower(), "left_control": {"x": 0.0, "y": 0.0},
             "right_control": {"x": 0.0, "y": 0.0}, "time_offset": int(beat_dur * 0.35), "values": [1.25 if is_even else 1.08]},
            {"curveType": "Line", "graphID": "", "id": str(uuid.uuid4()).lower(), "left_control": {"x": 0.0, "y": 0.0},
             "right_control": {"x": 0.0, "y": 0.0}, "time_offset": beat_dur, "values": [1.1 if is_even else 1.0]}
        ]

        tracks[0]["segments"].append({
            "id": seg_id,
            "material_id": vid_mat_id,
            "extra_material_refs": [speed_id],
            "target_timerange": {"start": i * beat_dur, "duration": beat_dur},
            "clip": {
                "alpha": 1.0, "rotation": 0.0,
                "scale": {"x": 1.0, "y": 1.0},
                "transform": {"x": 0.0, "y": 0.0}
            },
            "common_keyframes": [
                {"id": str(uuid.uuid4()).lower(), "keyframe_list": kf_list, "material_id": "", "property_type": "KFTypeScaleX"},
                {"id": str(uuid.uuid4()).lower(), "keyframe_list": kf_list, "material_id": "", "property_type": "KFTypeScaleY"}
            ],
            "speed": 1.0, "volume": 1.0
        })

        txt_mat_id = str(uuid.uuid4()).lower()
        cap_str = captions[i]
        clean_content = {
            "styles": [{
                "range": [0, len(cap_str)],
                "size": 10.0,
                "bold": True,
                "italic": False,
                "underline": False,
                "fill": {"alpha": 1.0, "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [0.0, 0.95, 1.0] if is_even else [1.0, 0.0, 0.4]}}}
            }],
            "text": cap_str
        }
        materials_texts.append({
            "id": txt_mat_id, "type": "text", "alignment": 1, "typesetting": 0, "check_flag": 7,
            "text_color": "#00F2FE" if is_even else "#FF0066", "font_size": 10.0,
            "content": json.dumps(clean_content, separators=(",", ":"), ensure_ascii=False)
        })
        tracks[1]["segments"].append({
            "id": str(uuid.uuid4()).lower(),
            "material_id": txt_mat_id,
            "extra_material_refs": [],
            "target_timerange": {"start": i * beat_dur, "duration": beat_dur},
            "clip": {
                "alpha": 1.0, "rotation": 0.0,
                "scale": {"x": 1.0, "y": 1.0},
                "transform": {"x": 0.0, "y": -0.65}
            },
            "common_keyframes": [],
            "speed": 1.0, "volume": 1.0
        })

    header_mat_id = str(uuid.uuid4()).lower()
    header_str = "JEDAG JEDUG VIRAL"
    header_content = {
        "styles": [{
            "range": [0, len(header_str)],
            "size": 15.0,
            "bold": True,
            "italic": False,
            "underline": False,
            "fill": {"alpha": 1.0, "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [1.0, 0.9, 0.0]}}}
        }],
        "text": header_str
    }
    materials_texts.insert(0, {
        "id": header_mat_id, "type": "text", "alignment": 1, "typesetting": 0, "check_flag": 7,
        "text_color": "#FFE500", "font_size": 15.0,
        "content": json.dumps(header_content, separators=(",", ":"), ensure_ascii=False)
    })
    tracks[1]["segments"].insert(0, {
        "id": str(uuid.uuid4()).lower(),
        "material_id": header_mat_id,
        "extra_material_refs": [],
        "target_timerange": {"start": 0, "duration": total_duration_us},
        "clip": {
            "alpha": 1.0, "rotation": 0.0,
            "scale": {"x": 1.0, "y": 1.0},
            "transform": {"x": 0.0, "y": 0.55}
        },
        "common_keyframes": [],
        "speed": 1.0, "volume": 1.0
    })

    if dst_audio.exists():
        aud_mat_id = str(uuid.uuid4()).lower()
        materials_audios.append({
            "id": aud_mat_id, "local_material_id": aud_mat_id, "type": "local_music",
            "category_name": "local", "path": str(dst_audio).replace("/", "\\"),
            "name": dst_audio.name, "duration": total_duration_us
        })
        meta_materials.append({
            "ai_group_type": "", "create_time": -1, "duration": total_duration_us, "enter_from": 0,
            "extra_info": dst_audio.name, "file_Path": f"./assets/audio/{dst_audio.name}", "height": 0,
            "id": aud_mat_id, "import_time": -1, "import_time_ms": -1, "item_source": 1,
            "material_color_tag": "", "md5": "", "metetype": "music",
            "roughcut_time_range": {"duration": -1, "start": -1},
            "sub_time_range": {"duration": -1, "start": -1}, "type": 0, "width": 0
        })
        tracks[2]["segments"].append({
            "id": str(uuid.uuid4()).lower(),
            "material_id": aud_mat_id,
            "extra_material_refs": [],
            "target_timerange": {"start": 0, "duration": total_duration_us},
            "source_timerange": {"start": 0, "duration": total_duration_us},
            "clip": {"alpha": 1.0, "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0}, "transform": {"x": 0.0, "y": 0.0}},
            "common_keyframes": [], "speed": 1.0, "volume": 0.8
        })

    draft_data = {
        "id": project_id,
        "duration": total_duration_us,
        "fps": 30.0,
        "canvas_config": {"height": 1920, "ratio": "9:16", "width": 1080},
        "tracks": tracks,
        "materials": {
            "videos": materials_videos,
            "texts": materials_texts,
            "speeds": materials_speeds,
            "audios": materials_audios,
            "transitions": [],
            "audio_fades": []
        },
        "platform": {"app_source": "cc", "app_version": "9.5.0", "os": "windows"},
        "last_modified_platform": {"app_source": "cc", "app_version": "9.5.0", "os": "windows"},
        "version": 360000
    }

    raw_content = json.dumps(draft_data, ensure_ascii=False, indent=2).encode("utf-8")

    (proj_dir / "draft_content.json").write_bytes(raw_content)
    (proj_dir / "template-2.tmp").write_bytes(raw_content)

    for old_bak in [proj_dir / "draft_content.json.bak", proj_dir / "draft_info.json.bak", proj_dir / "draft_meta_info.json.bak"]:
        if old_bak.exists():
            old_bak.unlink()

    info_data = {
        "id": project_id,
        "name": project_name,
        "duration": total_duration_us,
        "fps": 30,
        "canvas_config": draft_data["canvas_config"],
        "platform": draft_data["platform"],
        "tracks": tracks,
        "materials": draft_data["materials"],
        "extra_info": {}
    }
    (proj_dir / "draft_info.json").write_bytes(json.dumps(info_data, ensure_ascii=False, indent=2).encode("utf-8"))

    proj_json = {
        "config": {
            "color_space": -1, "hdr_vivid": False, "mixed_track_mode_on": False,
            "render_index_track_mode_on": False, "use_float_render": False
        },
        "create_time": now_us,
        "id": project_id,
        "main_timeline_id": project_id,
        "timelines": [{
            "create_time": now_us, "id": project_id, "is_marked_delete": False,
            "name": "Timeline 01", "update_time": now_us
        }],
        "update_time": now_us,
        "version": 0
    }
    (tl_dir / "project.json").write_bytes(json.dumps(proj_json, ensure_ascii=False, indent=2).encode("utf-8"))

    tl_sub = tl_dir / project_id
    tl_sub.mkdir(parents=True, exist_ok=True)
    (tl_sub / "draft_content.json").write_bytes(raw_content)
    (tl_sub / "template-2.tmp").write_bytes(raw_content)
    shutil.copy2(cover_file, tl_sub / "draft_cover.jpg")

    meta_data = {
        "draft_id": project_id,
        "draft_name": project_name,
        "draft_root_path": drafts_dir.as_posix(),
        "draft_fold_path": proj_dir.as_posix(),
        "draft_timeline_materials_size_": len(raw_content),
        "tm_duration": total_duration_us,
        "tm_draft_modified": now_us,
        "draft_materials": [{"type": 0, "value": meta_materials}]
    }
    (proj_dir / "draft_meta_info.json").write_bytes(json.dumps(meta_data, ensure_ascii=False, indent=2).encode("utf-8"))

    meta_path = drafts_dir / "root_meta_info.json"
    if meta_path.exists():
        try:
            root_data = json.loads(meta_path.read_text("utf-8"))
        except Exception:
            root_data = {"all_draft_store": [], "draft_ids": 0, "root_path": drafts_dir.as_posix()}
    else:
        root_data = {"all_draft_store": [], "draft_ids": 0, "root_path": drafts_dir.as_posix()}

    store = root_data.setdefault("all_draft_store", [])
    store = [x for x in store if x.get("draft_name") != project_name]

    cover_win = str(cover_file).replace("/", "\\")
    proj_win = str(proj_dir).replace("/", "\\")

    entry = {
        "cloud_draft_cover": False,
        "cloud_draft_sync": False,
        "draft_cloud_last_action_download": False,
        "draft_cloud_purchase_info": "",
        "draft_cloud_template_id": "",
        "draft_cloud_tutorial_info": "",
        "draft_cloud_videocut_purchase_info": "",
        "draft_cover": cover_win,
        "draft_fold_path": proj_win,
        "draft_id": project_id,
        "draft_is_ai_shorts": False,
        "draft_is_cloud_temp_draft": False,
        "draft_is_infinite_canvas_draft": False,
        "draft_is_invisible": False,
        "draft_is_pippit_draft": False,
        "draft_is_web_article_video": False,
        "draft_json_file": str(proj_dir / "draft_content.json").replace("/", "\\"),
        "draft_name": project_name,
        "draft_new_version": "",
        "draft_root_path": str(drafts_dir).replace("/", "\\"),
        "draft_timeline_materials_size": len(raw_content),
        "draft_type": "",
        "draft_web_article_video_enter_from": "",
        "pippit_avatar_url": "",
        "pippit_extra_info": "",
        "pippit_id": "",
        "pippit_user_name": "",
        "streaming_edit_draft_ready": True,
        "tm_draft_cloud_completed": "",
        "tm_draft_cloud_entry_id": 0,
        "tm_draft_cloud_modified": 0,
        "tm_draft_cloud_parent_entry_id": 0,
        "tm_draft_cloud_space_id": 0,
        "tm_draft_cloud_user_id": 0,
        "tm_draft_create": now_us,
        "tm_draft_modified": now_us,
        "tm_draft_removed": 0,
        "tm_duration": total_duration_us
    }
    store.insert(0, entry)
    root_data["all_draft_store"] = store
    meta_path.write_text(json.dumps(root_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"SUCCESS: Synced {project_name} (ID: {project_id})")


if __name__ == "__main__":
    # Primary project with active timeline ID
    sync_project("Jedag Jedug Beat Viral", "c1e9a4f2-7b83-4921-b0e6-d38a527fa119")
    # Fresh standalone project
    sync_project("Jedag Jedug Cyber 4K", "f1cd86e3-4246-4236-93cc-3c0f95a91d83")
