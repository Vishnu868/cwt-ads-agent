@echo off
echo ============================================
echo  CrowdWisdomTrading Ads AI Agent - Full Run
echo ============================================

cd /d V:\tzuroni\cwt-ads-agent

echo.
echo [1/2] Running Python pipeline (Agents 1-4)...
python main.py

echo.
echo [2/2] Rendering video with Remotion...
cd remotion_project
npx.cmd remotion render src/index.jsx CWTAd ../outputs/cwt_ad.mp4 --codec=h264

echo.
echo ============================================
echo  DONE! Video saved to outputs/cwt_ad.mp4
echo ============================================
pause