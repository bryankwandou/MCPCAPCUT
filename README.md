# mcp-capcut — MCP server untuk CapCut Desktop + editor web "Rakit Video"

Repo ini berdiri sendiri, terpisah dari MCP Canva ([bryankwandou/MCPCANVA](https://github.com/bryankwandou/MCPCANVA)).

| Bagian | Isi |
|---|---|
| **Server MCP** | Tool `capcut_*` (edit file project CapCut Desktop: buat project, tambah video/foto/audio/teks, geser/trim), `editor_*` (live editor + deploy ke CapCut), template, `catalog`, `desktop_*` (opsional) |
| **Editor web** | `src/creative_mcp/editor/`: editor video bergaya CapCut (timeline, keyframe, teks, stiker, efek, filter, transisi, musik). Dideploy ke Vercel sebagai situs statis |
| **Daftar fitur** | `FEATURES.md` / `features.html`: fitur CapCut Free vs Pro dan status di editor ini |

CapCut tidak punya API publik: tool bekerja pada file project lokal (tutup project di CapCut dulu; backup `*.json.bak` otomatis).
Beberapa versi CapCut mengenkripsi project; untuk itu pakai `desktop_*`. Fitur Pro tidak dibuka tanpa langganan.

## Instalasi (di komputer yang ada CapCut Desktop)
```bash
git clone https://github.com/bryankwandou/MCPCAPCUT && cd MCPCAPCUT
pip install -e ".[desktop]"
```
Claude Desktop (`claude_desktop_config.json`):
```json
{ "mcpServers": { "capcut": { "command": "mcp-capcut" } } }
```
Editor live: `mcp-capcut editor <nama-project>`.

## Cek koneksi
```bash
python scripts/verify_connection.py --write
```
Berhasil bila project `tes-mcp-…` muncul di CapCut dengan teks "Halo dari MCP".

## Deploy editor ke Vercel
Import repo ini di Vercel; `vercel.json` sudah menyetel output `src/creative_mcp/editor` tanpa build.
