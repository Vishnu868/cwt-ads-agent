import React from 'react';
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
