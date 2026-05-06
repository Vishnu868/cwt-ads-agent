import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

const SCENE_ICONS = ['📈', '💡', '🎯', '🔔', '💰', '🚀', '✅', '⚡'];

export const CWTVideoScene = ({ text, sceneIndex, primary, accent, bg }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 15], [0, 1]);
  const y = interpolate(frame, [0, 15], [30, 0]);
  const icon = SCENE_ICONS[sceneIndex % SCENE_ICONS.length];

  return (
    <AbsoluteFill style={{
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      flexDirection: 'column', padding: '60px 40px',
      opacity, transform: `translateY(${y}px)`,
    }}>
      <div style={{
        fontSize: 80, marginBottom: 30,
        filter: `drop-shadow(0 0 20px ${primary})`,
      }}>
        {icon}
      </div>
      <div style={{
        fontSize: 52, fontWeight: 700, color: '#FFFFFF',
        textAlign: 'center', lineHeight: 1.3,
        fontFamily: 'Arial, sans-serif',
        textShadow: `0 2px 20px rgba(0,0,0,0.8)`,
        maxWidth: 900,
      }}>
        {text}
      </div>
    </AbsoluteFill>
  );
};
