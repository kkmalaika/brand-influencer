@echo off
cd /d F:\PYTHON\brand-influencer

call .venv\Scripts\activate

REM Ensure logs folder exists
if not exist logs mkdir logs

REM Add timestamp header
echo ===================== %date% %time% ===================== >> logs\fetch_tiktok_stats.log

REM Run daily TikTok stats fetch
python manage.py fetch_tiktok_stats_apify >> logs\fetch_tiktok_stats.log 2>&1

REM Add footer
echo. >> logs\fetch_tiktok_stats.log
echo ----------------------------------------------------------- >> logs\fetch_tiktok_stats.log
