#!/bin/bash
cd V:\tzuroni\cwt-ads-agent\remotion_project
npm install --legacy-peer-deps
npx remotion render CWTAd V:\tzuroni\cwt-ads-agent\outputs\cwt_ad.mp4 --codec=h264
