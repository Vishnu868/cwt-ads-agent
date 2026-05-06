"""
tools/remotion_builder.py
Orchestrates Remotion video rendering with voiceover, subtitles, and visuals.
Writes the Remotion React project, installs deps, and renders the final MP4.
"""
import json
import os
import subprocess
import time
from pathlib import Path
from typing import Optional

from loguru import logger

from config.settings import OUTPUT_DIR, REMOTION_PROJECT_DIR


# ─── Remotion project scaffolding ────────────────────────────────────────────

def write_remotion_project(script_data: dict, audio_path=None) -> Path:
    project_dir = REMOTION_PROJECT_DIR
    project_dir.mkdir(parents=True, exist_ok=True)
    src_dir = project_dir / "src"
    src_dir.mkdir(exist_ok=True)
    public_dir = project_dir / "public"
    public_dir.mkdir(exist_ok=True)

    # Copy audio file only — never overwrite JSX files
    if audio_path and Path(audio_path).exists():
        import shutil
        dest = public_dir / "voiceover.mp3"
        shutil.copy(audio_path, dest)
        logger.info(f"Audio copied → {dest}")

    # Only write JSX files if they don't already exist
    if not (src_dir / "Root.jsx").exists():
        _write_package_json(project_dir)
        _write_root_component(src_dir, script_data, "voiceover.mp3", 30, 1800, "#00C2FF", "#FFD700", "#0A0A1A")
        _write_index(src_dir, 30, 1800)
        _write_video_component(src_dir, script_data, 30, "#00C2FF", "#FFD700", "#0A0A1A")
        _write_subtitle_component(src_dir)
    else:
        _write_package_json(project_dir)

    logger.success(f"Remotion project written → {project_dir}")
    return project_dir

def _write_package_json(project_dir: Path) -> None:
    pkg = {
        "name": "cwt-ad-video",
        "version": "1.0.0",
        "description": "CrowdWisdomTrading Ad Video",
        "scripts": {
            "start": "remotion studio",
            "build": "remotion render CWTAd out/video.mp4",
            "render": "remotion render CWTAd out/video.mp4 --codec=h264"
        },
        "dependencies": {
            "remotion": "^4.0.0",
            "@remotion/player": "^4.0.0",
            "@remotion/cli": "^4.0.0",
            "react": "^18.0.0",
            "react-dom": "^18.0.0"
        },
        "devDependencies": {
            "@types/react": "^18.0.0",
            "typescript": "^5.0.0"
        }
    }
    (project_dir / "package.json").write_text(
        json.dumps(pkg, indent=2), encoding="utf-8"
    )


def _write_root_component(
    src_dir: Path,
    script_data: dict,
    audio_ref: str,
    fps: int,
    total_frames: int,
    primary: str,
    accent: str,
    bg: str,
) -> None:
    scenes = script_data.get("scenes", [])
    hook_text = script_data.get("hook", "")
    cta_text = script_data.get("cta", "Join CrowdWisdomTrading Today")

    scenes_js = json.dumps(scenes)

    audio_tag = f'<Audio src={{staticFile("{audio_ref}")}} />' if audio_ref else ""
    audio_import = "import { Audio, staticFile } from 'remotion';" if audio_ref else ""

    jsx = f"""import React from 'react';
import {{ AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, interpolate, spring }} from 'remotion';
{audio_import}
import {{ CWTVideoScene }} from './VideoComponent';
import {{ Subtitle }} from './SubtitleComponent';

const SCENES = {scenes_js};
const FPS = {fps};

export const CWTAd = () => {{
  const frame = useCurrentFrame();
  const {{ durationInFrames }} = useVideoConfig();

  return (
    <AbsoluteFill style={{{{ backgroundColor: '{bg}' }}}}>
      {audio_tag}

      {{/* HOOK — first 90 frames (3s) */}}
      <Sequence from={{0}} durationInFrames={{{{90}}}}>
        <HookScene text={{{{"{hook_text}"}}}} primary={{{{'{primary}'}}}} accent={{{{'{accent}'}}}} />
      </Sequence>

      {{/* BODY SCENES */}}
      {{SCENES.map((scene, i) => {{
        const start = 90 + SCENES.slice(0, i).reduce((a, s) => a + s.duration_secs * FPS, 0);
        const duration = scene.duration_secs * FPS;
        return (
          <Sequence key={{i}} from={{{{start}}}} durationInFrames={{{{duration}}}}>
            <CWTVideoScene
              text={{{{scene.text}}}}
              sceneIndex={{{{i}}}}
              primary={{{{'{primary}'}}}}
              accent={{{{'{accent}'}}}}
              bg={{{{'{bg}'}}}}
            />
          </Sequence>
        );
      }})}}

      {{/* CTA — last 90 frames (3s) */}}
      <Sequence from={{{{durationInFrames - 90}}}} durationInFrames={{{{90}}}}>
        <CTAScene text={{{{"{cta_text}"}}}} primary={{{{'{primary}'}}}} accent={{{{'{accent}'}}}} />
      </Sequence>

      {{/* SUBTITLES OVERLAY */}}
      <Subtitle scenes={{{{SCENES}}}} hookText={{{{"{hook_text}"}}}} ctaText={{{{"{cta_text}"}}}} fps={{{{FPS}}}} />
    </AbsoluteFill>
  );
}};

const HookScene = ({{ text, primary, accent }}) => {{
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 20], [0, 1]);
  const scale = interpolate(frame, [0, 20], [0.8, 1]);

  return (
    <AbsoluteFill style={{{{
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      flexDirection: 'column', opacity,
      background: `radial-gradient(ellipse at center, ${{primary}}22 0%, transparent 70%)`,
    }}}}>
      <div style={{{{
        fontSize: 72, fontWeight: 900, color: accent,
        textAlign: 'center', padding: '0 60px',
        transform: `scale(${{scale}})`,
        textShadow: `0 0 40px ${{primary}}`,
        fontFamily: 'Arial Black, sans-serif',
        lineHeight: 1.2,
      }}}}>
        {{text}}
      </div>
    </AbsoluteFill>
  );
}};

const CTAScene = ({{ text, primary, accent }}) => {{
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 20], [0, 1]);
  const pulse = interpolate(frame % 30, [0, 15, 30], [1, 1.03, 1]);

  return (
    <AbsoluteFill style={{{{
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      flexDirection: 'column', opacity,
      background: `linear-gradient(135deg, ${{primary}}33, transparent)`,
    }}}}>
      <div style={{{{
        background: primary, color: '#000', fontWeight: 900,
        fontSize: 52, padding: '30px 60px', borderRadius: 16,
        transform: `scale(${{pulse}})`,
        boxShadow: `0 0 60px ${{primary}}`,
        fontFamily: 'Arial Black, sans-serif',
        textAlign: 'center',
      }}}}>
        {{text}}
      </div>
      <div style={{{{ color: accent, fontSize: 28, marginTop: 20, fontFamily: 'Arial, sans-serif' }}}}>
        crowdwisdomtrading.com
      </div>
    </AbsoluteFill>
  );
}};
"""
    (src_dir / "Root.jsx").write_text(jsx, encoding="utf-8")


def _write_index(src_dir: Path, fps: int, total_frames: int) -> None:
    content = f"""import {{ registerRoot }} from 'remotion';
import React from 'react';
import {{ Composition }} from 'remotion';
import {{ CWTAd }} from './Root';

registerRoot(() => (
  <>
    <Composition
      id="CWTAd"
      component={{CWTAd}}
      durationInFrames={{{total_frames}}}
      fps={{{fps}}}
      width={{1080}}
      height={{1920}}
    />
  </>
));
"""
    (src_dir / "index.jsx").write_text(content, encoding="utf-8")


def _write_video_component(
    src_dir: Path, script_data: dict, fps: int, primary: str, accent: str, bg: str
) -> None:
    jsx = f"""import React from 'react';
import {{ AbsoluteFill, useCurrentFrame, interpolate }} from 'remotion';

const SCENE_ICONS = ['📈', '💡', '🎯', '🔔', '💰', '🚀', '✅', '⚡'];

export const CWTVideoScene = ({{ text, sceneIndex, primary, accent, bg }}) => {{
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 15], [0, 1]);
  const y = interpolate(frame, [0, 15], [30, 0]);
  const icon = SCENE_ICONS[sceneIndex % SCENE_ICONS.length];

  return (
    <AbsoluteFill style={{{{
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      flexDirection: 'column', padding: '60px 40px',
      opacity, transform: `translateY(${{y}}px)`,
    }}}}>
      <div style={{{{
        fontSize: 80, marginBottom: 30,
        filter: `drop-shadow(0 0 20px ${{primary}})`,
      }}}}>
        {{icon}}
      </div>
      <div style={{{{
        fontSize: 52, fontWeight: 700, color: '#FFFFFF',
        textAlign: 'center', lineHeight: 1.3,
        fontFamily: 'Arial, sans-serif',
        textShadow: `0 2px 20px rgba(0,0,0,0.8)`,
        maxWidth: 900,
      }}}}>
        {{text}}
      </div>
    </AbsoluteFill>
  );
}};
"""
    (src_dir / "VideoComponent.jsx").write_text(jsx, encoding="utf-8")


def _write_subtitle_component(src_dir: Path) -> None:
    jsx = """import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';

export const Subtitle = ({ scenes, hookText, ctaText, fps }) => {
  const frame = useCurrentFrame();
  const FPS = fps || 30;

  // Build full subtitle timeline
  const timeline = [];
  // Hook (0-90 frames)
  timeline.push({ start: 0, end: 90, text: hookText });

  let offset = 90;
  for (const scene of scenes) {
    const dur = scene.duration_secs * FPS;
    // Split long text into chunks of ~8 words
    const words = scene.text.split(' ');
    const chunkSize = 8;
    const chunks = [];
    for (let i = 0; i < words.length; i += chunkSize) {
      chunks.push(words.slice(i, i + chunkSize).join(' '));
    }
    const chunkFrames = Math.floor(dur / chunks.length);
    chunks.forEach((chunk, ci) => {
      timeline.push({
        start: offset + ci * chunkFrames,
        end: offset + (ci + 1) * chunkFrames,
        text: chunk,
      });
    });
    offset += dur;
  }

  const current = timeline.find(t => frame >= t.start && frame < t.end);
  if (!current || !current.text) return null;

  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      <div style={{
        position: 'absolute', bottom: 160, left: 0, right: 0,
        display: 'flex', justifyContent: 'center', padding: '0 40px',
      }}>
        <div style={{
          backgroundColor: 'rgba(0,0,0,0.75)',
          color: '#FFFFFF',
          fontSize: 40,
          fontWeight: 700,
          padding: '16px 32px',
          borderRadius: 12,
          textAlign: 'center',
          maxWidth: 960,
          fontFamily: 'Arial, sans-serif',
          lineHeight: 1.4,
          border: '2px solid rgba(255,255,255,0.15)',
        }}>
          {current.text}
        </div>
      </div>
    </AbsoluteFill>
  );
};
"""
    (src_dir / "SubtitleComponent.jsx").write_text(jsx, encoding="utf-8")


def render_video(project_dir: Path, output_path: Optional[Path] = None) -> Path:
    """
    Install Remotion deps and render the video.
    Returns path to rendered MP4.
    """
    if output_path is None:
        output_path = OUTPUT_DIR / "cwt_ad.mp4"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info("Installing Remotion dependencies...")
    npm_install = subprocess.run(
        ["npm.cmd", "install", "--legacy-peer-deps"],
        cwd=project_dir,
        capture_output=True,
        text=True,
        timeout=180,
    )
    if npm_install.returncode != 0:
        logger.warning(f"npm install stderr: {npm_install.stderr[-500:]}")
        # Continue anyway — may already be installed

    logger.info(f"Rendering Remotion video → {output_path}")
    render_cmd = [
        "npx.cmd", "remotion", "render", "src/index.jsx", "CWTAd",
        str(output_path),
        "--codec=h264",
    ]
    result = subprocess.run(
        render_cmd,
        cwd=project_dir,
        capture_output=True,
        text=True,
        timeout=600,
    )

    if result.returncode == 0:
        logger.success(f"Video rendered → {output_path}")
    else:
        logger.error(f"Remotion render failed:\n{result.stderr[-1000:]}")
        # Write render command for manual use
        script_path = OUTPUT_DIR / "render.sh"
        script_path.write_text(
            f"#!/bin/bash\ncd {project_dir}\nnpm install --legacy-peer-deps\nnpx remotion render CWTAd {output_path} --codec=h264\n"
        )
        logger.info(f"Render script saved → {script_path} (run manually if needed)")

    return output_path