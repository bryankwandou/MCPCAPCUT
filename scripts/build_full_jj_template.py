import os
import sys
import subprocess
import json
from pathlib import Path

DRAFTS_DIR = Path(r"C:\Users\arche\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft")

def run_cmd(cmd_list):
    # Properly quote arguments that have spaces
    escaped = []
    for arg in cmd_list:
        a = str(arg)
        if " " in a and not (a.startswith('"') and a.endswith('"')):
            escaped.append(f'"{a}"')
        else:
            escaped.append(a)
    joined = " ".join(escaped)
    print(f">> Executing: {joined}")
    res = subprocess.run(joined, capture_output=True, text=True, shell=True)
    if res.returncode != 0:
        print(f"Error (code {res.returncode}):\n{res.stderr}\n{res.stdout}")
    else:
        print(f"Success:\n{res.stdout.strip()[:300]}")
    return res

def build_template(draft_name: str):
    draft_path = DRAFTS_DIR / draft_name
    print(f"\n==========================================")
    print(f"Building Full CapCut Template: {draft_name}")
    print(f"Target Path: {draft_path}")
    print(f"==========================================")

    # 1. Clean existing folder if needed
    if draft_path.exists():
        import shutil
        print(f"Backing up and resetting {draft_path}...")
        try:
            shutil.rmtree(draft_path, ignore_errors=True)
        except Exception as e:
            print(f"Warning on rmtree: {e}")

    # 2. Init fresh 9:16 vertical draft
    res = run_cmd(["npx", "capcut-cli", "init", draft_name, "--ratio", "9:16", "--force-write"])
    if res.returncode != 0:
        print(f"Failed to init draft {draft_name}")
        return False

    # 3. Source assets from cache or sample
    fallback_video_dir = Path(r"e:\000VSCODE PROJECT MULAI DARI DESEMBER 2025\MCPCAPCUT\assets\video")
    fallback_audio_dir = Path(r"e:\000VSCODE PROJECT MULAI DARI DESEMBER 2025\MCPCAPCUT\assets\audio")
    
    candidate_img_dirs = [
        DRAFTS_DIR / "_cache_media",
        DRAFTS_DIR / "Jedag Jedug Beat Viral" / "assets" / "video",
        fallback_video_dir
    ]
    img_files = []
    for cd in candidate_img_dirs:
        if cd.exists():
            found = list(cd.glob("*.jpg")) + list(cd.glob("*.png"))
            if len(found) >= 5:
                img_files = sorted(found, key=lambda p: p.name)
                print(f"Using {len(img_files)} images from {cd}")
                break

    if not img_files:
        print("Error: No images found to build template!")
        return False

    candidate_audio = [
        DRAFTS_DIR / "_cache_media" / "v1-music.wav",
        DRAFTS_DIR / "Jedag Jedug Beat Viral" / "assets" / "audio" / "v1-music.wav",
        fallback_audio_dir / "v1-music.wav"
    ]
    audio_path = None
    for ca in candidate_audio:
        if ca.exists():
            audio_path = ca
            print(f"Using audio from {audio_path}")
            break

    # Clip specifications: (start_s, duration_s, title, intro_anim, transition_slug, effect_slug)
    specs = [
        (0.0, 1.5, "JEDAG JEDUG VIRAL", "zoom-out", "white-flash", None),
        (1.5, 0.7, "BASS DROP", "flash-in", "flash", "shake"),
        (2.2, 0.7, "CYBER BEAT", "pulsing-zooms", "strobe", None),
        (2.9, 0.7, "TURBO MODE", "zoom-out", "glitch", "strobe"),
        (3.6, 0.7, "HYPE VIBES", "flash-in", "white-flash", None),
        (4.3, 0.7, "MAX ENERGY", "pulsing-zooms", "flash", "shake"),
        (5.0, 0.7, "NEON CITY", "zoom-out", "strobe", None),
        (5.7, 0.7, "TOKYO DRIFT", "flash-in", "glitch", "chromatic"),
        (6.4, 0.7, "OVERDRIVE", "pulsing-zooms", "white-flash", None),
        (7.1, 0.8, "DROP THE BASS", "fade-in", None, "explosion"),
    ]

    total_duration = 7.9
    seg_ids = []

    # 4. Add video segments
    for i, (start_s, dur_s, text_val, anim_slug, trans_slug, eff_slug) in enumerate(specs):
        img = img_files[i % len(img_files)]
        print(f"\nAdding video clip [{i}] at {start_s}s ({dur_s}s) - {img.name}")
        cmd = ["npx", "capcut-cli", "add-video", str(draft_path), str(img), str(start_s), str(dur_s), "--force-write"]
        res = run_cmd(cmd)
        try:
            data = json.loads(res.stdout)
            seg_id = data.get("segment_id")
            seg_ids.append((i, seg_id, trans_slug, anim_slug, eff_slug, start_s, dur_s, text_val))
        except Exception as e:
            print(f"Failed to parse add-video output: {e}")

    # 5. Add transitions between clips
    print("\n--- Attaching Transitions ---")
    for i, seg_id, trans_slug, anim_slug, eff_slug, start_s, dur_s, text_val in seg_ids:
        if trans_slug and i < len(seg_ids) - 1:
            print(f"Attaching transition '{trans_slug}' to clip [{i}] (id: {seg_id})")
            cmd = ["npx", "capcut-cli", "transition", str(draft_path), seg_id, trans_slug, "--force-write"]
            run_cmd(cmd)

    # 6. Add clip animations
    print("\n--- Attaching Clip Animations ---")
    for i, seg_id, trans_slug, anim_slug, eff_slug, start_s, dur_s, text_val in seg_ids:
        if anim_slug:
            print(f"Attaching animation '{anim_slug}' to clip [{i}] (id: {seg_id})")
            cmd = ["npx", "capcut-cli", "image-anim", str(draft_path), seg_id, "--intro", anim_slug, "--intro-duration", "0.4", "--force-write"]
            run_cmd(cmd)

    # 7. Add scene effects on timeline
    print("\n--- Adding Scene Effects ---")
    for i, seg_id, trans_slug, anim_slug, eff_slug, start_s, dur_s, text_val in seg_ids:
        if eff_slug:
            print(f"Adding scene effect '{eff_slug}' at {start_s}s ({dur_s}s)")
            cmd = ["npx", "capcut-cli", "add-effect", str(draft_path), eff_slug, str(start_s), str(dur_s), "--force-write"]
            run_cmd(cmd)

    # 8. Add active Color Filter across timeline
    print("\n--- Adding Color Filter ---")
    cmd = ["npx", "capcut-cli", "add-filter", str(draft_path), "vivid", "--full", "--force-write"]
    run_cmd(cmd)

    # 9. Add background music track
    if audio_path:
        print(f"\n--- Adding Background Music: {audio_path.name} ---")
        cmd = ["npx", "capcut-cli", "add-audio", str(draft_path), str(audio_path), "0", str(total_duration), "--force-write"]
        run_cmd(cmd)

    # 10. Add stylish text segments
    print("\n--- Adding Animated Text Headers ---")
    for i, seg_id, trans_slug, anim_slug, eff_slug, start_s, dur_s, text_val in seg_ids:
        cmd = ["npx", "capcut-cli", "add-text", str(draft_path), str(start_s), str(dur_s), text_val, "--font-size", "14", "--color", "#FFFFFF", "--y", "-0.7", "--force-write"]
        run_cmd(cmd)

    # 11. Reconcile all timeline mirrors (root + nested Timelines)
    print("\n--- Reconciling Timeline Mirrors ---")
    cmd = ["npx", "capcut-cli", "sync-timelines", str(draft_path), "--nested", "--apply", "--force-write"]
    run_cmd(cmd)

    # 12. Register project in CapCut master index and local media catalog
    print("\n--- Registering in CapCut Store & Materials ---")
    cmd = ["npx", "capcut-cli", "register", str(draft_path), "--apply", "--materials", "--force-write"]
    run_cmd(cmd)

    # 13. Diagnose final draft
    print("\n--- Running Final Draft Verification ---")
    cmd = ["npx", "capcut-cli", "diagnose", str(draft_path)]
    run_cmd(cmd)

    # 14. Print track summary
    cmd = ["npx", "capcut-cli", "tracks", str(draft_path)]
    run_cmd(cmd)

    print(f"\nDraft '{draft_name}' successfully built and verified!")
    return True

if __name__ == "__main__":
    media_cache = DRAFTS_DIR / "_cache_media"
    media_cache.mkdir(parents=True, exist_ok=True)
    
    # Save cache of media if exists
    src_v = DRAFTS_DIR / "Jedag Jedug Cyber 4K" / "assets" / "video"
    if src_v.exists():
        for f in src_v.glob("*.jpg"):
            import shutil
            shutil.copy2(f, media_cache / f.name)
    src_a = DRAFTS_DIR / "Jedag Jedug Cyber 4K" / "assets" / "audio"
    if src_a.exists():
        for f in src_a.glob("*.wav"):
            import shutil
            shutil.copy2(f, media_cache / f.name)

    # Build both projects
    build_template("Jedag Jedug Cyber 4K")
    build_template("Jedag Jedug Beat Viral")
