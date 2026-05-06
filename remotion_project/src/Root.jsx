import React from 'react';
import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, interpolate } from 'remotion';
import { CWTVideoScene } from './VideoComponent';
import { Subtitle } from './SubtitleComponent';

const SCENES = [
  { text: "Most traders fail — not because they're not smart", duration_secs: 6 },
  { text: "But because they have NO edge and NO signals", duration_secs: 7 },
  { text: "Introducing CrowdWisdomTrading", duration_secs: 5 },
  { text: "10,000+ traders sharing real-time buy/sell alerts daily", duration_secs: 8 },
  { text: "Alerts BEFORE the market moves. Daily watchlists. Live Q&A.", duration_secs: 8 },
  { text: "Last month: top alerts averaged 12% gains", duration_secs: 7 },
  { text: "Join FREE for 7 days — no commitment", duration_secs: 7 },
];

const HOOK = "Still losing trades because you're trading alone?";
const CTA = "Join FREE → crowdwisdomtrading.com";
const PRIMARY = "#00C2FF";
const ACCENT = "#FFD700";
const BG = "#0A0A1A";
const FPS = 30;

export const CWTAd = () => {
  const { durationInFrames } = useVideoConfig();

  let offset = 90;
  const sceneSequences = SCENES.map((scene, i) => {
    const start = offset;
    const duration = scene.duration_secs * FPS;
    offset += duration;
    return { start, duration, text: scene.text, index: i };
  });

  return (
    <AbsoluteFill style={{ backgroundColor: BG }}>

      {/* HOOK — first 3 seconds */}
      <Sequence from={0} durationInFrames={90}>
        <HookScene text={HOOK} />
      </Sequence>

      {/* BODY SCENES */}
      {sceneSequences.map((s) => (
        <Sequence key={s.index} from={s.start} durationInFrames={s.duration}>
          <CWTVideoScene text={s.text} sceneIndex={s.index} primary={PRIMARY} accent={ACCENT} bg={BG} />
        </Sequence>
      ))}

      {/* CTA — last 3 seconds */}
      <Sequence from={durationInFrames - 90} durationInFrames={90}>
        <CTAScene text={CTA} />
      </Sequence>

      {/* SUBTITLES */}
      <Subtitle scenes={SCENES} hookText={HOOK} ctaText={CTA} fps={FPS} />
    </AbsoluteFill>
  );
};

const HookScene = ({ text }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const scale = interpolate(frame, [0, 20], [0.85, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexDirection: 'column',
      opacity,
      background: 'radial-gradient(ellipse at center, rgba(0,194,255,0.15) 0%, transparent 70%)',
    }}>
      <div style={{
        fontSize: 68,
        fontWeight: 900,
        color: ACCENT,
        textAlign: 'center',
        padding: '0 60px',
        transform: `scale(${scale})`,
        textShadow: `0 0 40px ${PRIMARY}`,
        fontFamily: 'Arial Black, sans-serif',
        lineHeight: 1.2,
      }}>
        {text}
      </div>
    </AbsoluteFill>
  );
};

const CTAScene = ({ text }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const pulse = interpolate(frame % 30, [0, 15, 30], [1, 1.03, 1]);

  return (
    <AbsoluteFill style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexDirection: 'column',
      opacity,
      background: 'linear-gradient(135deg, rgba(0,194,255,0.2), transparent)',
    }}>
      <div style={{
        background: PRIMARY,
        color: '#000',
        fontWeight: 900,
        fontSize: 52,
        padding: '30px 60px',
        borderRadius: 16,
        transform: `scale(${pulse})`,
        boxShadow: `0 0 60px ${PRIMARY}`,
        fontFamily: 'Arial Black, sans-serif',
        textAlign: 'center',
      }}>
        {text}
      </div>
      <div style={{
        color: ACCENT,
        fontSize: 28,
        marginTop: 20,
        fontFamily: 'Arial, sans-serif',
      }}>
        crowdwisdomtrading.com
      </div>
    </AbsoluteFill>
  );
};