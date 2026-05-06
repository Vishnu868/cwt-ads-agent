import { registerRoot } from 'remotion';
import React from 'react';
import { Composition } from 'remotion';
import { CWTAd } from './Root';

registerRoot(() => (
  <>
    <Composition
      id="CWTAd"
      component={CWTAd}
      durationInFrames={1680}
      fps={30}
      width={1080}
      height={1920}
    />
  </>
));
