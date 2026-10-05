# Linux Readiness Check

Öffentliches Repo der App [Linux Readiness Check](https://frumpellabs.de/linux-readiness-check) von Frumpel Labs, die einschätzt, wie gut ein Windows-PC für einen Umstieg auf Linux vorbereitet ist.

## Download

Die aktuelle Version findest du unter **[Releases](https://github.com/MaBeink/linux-readiness-check-public/releases/latest)**: den Windows-Installer (Datei endet auf `_x64-setup.exe`, für ARM-Geräte auf `_arm64-setup.exe`), Linux-Pakete (`.AppImage`, `.deb`, jeweils für x64 und ARM64) und `SHA256SUMS.txt` zum Prüfen. Neuere Versionen kannst du danach direkt in der App installieren.

## Programmliste

- **`rules.json`**: die Bewertungen. Die App lädt sie, wenn auf dem Startbildschirm „Liste und Updates laden“ gesetzt ist.
- **`pending.json`**: Programme, für die noch Erfahrungen fehlen. Die App zeigt sie unter „Programme bewerten“.

Beim Laden dieser Dateien sendet die App keine Daten über deinen PC.

## Mitmachen

Du kennst ein Programm unter Linux? Am einfachsten bewertest du es direkt in der App unter „Programme bewerten“. Alternativ kannst du ein Issue mit der Vorlage „Programm bewerten“ öffnen oder einen Pull Request stellen. Details stehen in [CONTRIBUTING.md](CONTRIBUTING.md).

## Lizenz

Die Daten in diesem Repo stehen unter [CC BY 4.0](LICENSE). Du darfst sie mit Namensnennung („Linux Readiness Check rule data“ von Frumpel Labs) frei verwenden.

---

## English

Public repository of the app [Linux Readiness Check](https://frumpellabs.de/linux-readiness-check) by Frumpel Labs, which assesses how well a Windows PC is prepared for switching to Linux.

- **Download:** the current version is under **[Releases](https://github.com/MaBeink/linux-readiness-check-public/releases/latest)**: the Windows installer (file ending in `_x64-setup.exe`, for ARM devices `_arm64-setup.exe`), Linux packages (`.AppImage`, `.deb`, each for x64 and ARM64) and `SHA256SUMS.txt` for checking. Later versions can be installed directly in the app.
- **`rules.json`:** the ratings. The app loads them when “Load list and updates” is ticked on the start screen.
- **`pending.json`:** programs that still lack experience reports. The app shows them under “Rate programs”.
- Loading these files sends no data about your PC.
- **Contributing:** the easiest way is to rate programs directly in the app under “Rate programs”. You can also open an issue with the “Programm bewerten / Rate a program” template or a pull request, see [CONTRIBUTING.md](CONTRIBUTING.md).
- **License:** the data in this repository is licensed under [CC BY 4.0](LICENSE) (“Linux Readiness Check rule data” by Frumpel Labs).
