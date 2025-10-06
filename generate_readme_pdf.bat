@echo off
title ZenDegenAcademy - README PDF Generator
color 0A

echo.
echo  ███████╗███████╗███╗   ██╗██████╗ ███████╗ ██████╗ ███████╗███╗   ██╗
echo  ╚══███╔╝██╔════╝████╗  ██║██╔══██╗██╔════╝██╔════╝ ██╔════╝████╗  ██║
echo    ███╔╝ █████╗  ██╔██╗ ██║██║  ██║█████╗  ██║  ███╗█████╗  ██╔██╗ ██║
echo   ███╔╝  ██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██║   ██║██╔══╝  ██║╚██╗██║
echo  ███████╗███████╗██║ ╚████║██████╔╝███████╗╚██████╔╝███████╗██║ ╚████║
echo  ╚══════╝╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝
echo.
echo                        📄 README PDF Generator 🚀
echo.
echo ================================================================================
echo.

echo 📁 Current directory: %CD%
echo 📄 Converting README.md to HTML...
echo.

REM Konwertuj README do HTML
python convert_readme_to_pdf.py

echo.
echo 🌐 Opening README.html in browser...
echo.

REM Otwórz plik HTML w przeglądarce
start README.html

echo.
echo ================================================================================
echo 📝 INSTRUKCJA ZAPISYWANIA DO PDF:
echo.
echo 1. 🌐 Plik README.html został otwarty w przeglądarce
echo 2. 🖨️  Naciśnij Ctrl+P (lub F12 i wybierz Drukuj)
echo 3. 🎯 Wybierz "Zapisz jako PDF" jako miejsce docelowe
echo 4. ⚙️  Ustaw orientację na "Pionowa" 
echo 5. 📏 Ustaw marginesy na "Minimum" lub "Niestandardowe"
echo 6. ✅ Kliknij "Zapisz" i wybierz lokalizację
echo.
echo 💡 WSKAZÓWKI:
echo    - Sprawdź podgląd przed zapisaniem
echo    - Możesz wyłączyć nagłówki i stopki strony
echo    - Kolory będą zachowane w PDF
echo    - Rozmiar pliku będzie około 1-2 MB
echo.
echo ================================================================================
echo.

pause