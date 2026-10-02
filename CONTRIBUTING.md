# Mitmachen

Danke, dass du helfen möchtest! Jede Bewertung hilft Menschen, die über einen Umstieg von Windows auf Linux nachdenken.

## Der einfachste Weg: in der App bewerten

In Linux Readiness Check links in der Seitenleiste „Programme bewerten“ öffnen, die Liste laden und Programme bewerten, die du unter Linux selbst ausprobiert hast. Die App zeigt dir vor dem Senden genau, was gesendet wird.

## Per Issue

Öffne ein Issue mit der Vorlage **„Programm bewerten“**. Bitte nur Programme bewerten, die du selbst unter Linux genutzt hast.

## Per Pull Request

Änderungen an `rules.json` sind willkommen. Bitte pro Pull Request nur wenige Programme und kurz begründen, woher die Einschätzung stammt.

### Format einer Regel

```json
{
  "name": "Affinity Photo",
  "aliases": ["Affinity Photo 2"],
  "readiness": "red",
  "category": "Creative",
  "reason": "Keine native Linux-Version. Über Wine nur eingeschränkt nutzbar.",
  "reason_en": "No native Linux version. Only partly usable via Wine.",
  "alternatives": ["GIMP", "Krita", "Photopea"]
}
```

| Feld | Pflicht | Bedeutung |
|---|---|---|
| `name` | ja | Name, wie er unter Windows installiert erscheint |
| `aliases` | nein | Weitere Schreibweisen, unter denen das Programm erkannt werden soll |
| `readiness` | ja | Einstufung, siehe unten |
| `category` | ja | Kategorie, zum Beispiel `Office`, `Gaming`, `Creative`, `Development` |
| `reason` | ja | Kurze, verständliche Begründung auf Deutsch, ein bis zwei Sätze |
| `alternatives` | nein | Linux-Alternativen oder Lösungswege |
| `reason_en` | nein | Dieselbe Begründung auf Englisch; ohne sie zeigt die englische App den deutschen Text |
| `alternatives_en` | nein | Nur nötig, wenn Alternativen deutsche Wörter enthalten (zum Beispiel „ProtonDB prüfen“ → „check ProtonDB“) |

### Einstufungen

| `readiness` | In der App | Bedeutung |
|---|---|---|
| `green` | läuft | Native Linux-Version oder läuft problemlos |
| `yellow` | Umweg | Läuft mit Einschränkungen, per Web-Version, Wine/Proton oder mit einer guten Alternative |
| `red` | schwierig | Läuft nicht oder nur mit großem Aufwand; kann einen Umstieg verhindern |

Programme ohne Regel zeigt die App als „unbekannt“; dafür braucht es keinen Eintrag.

### Wichtig

- Nach jeder Änderung `rules_version` am Anfang von `rules.json` erhöhen (Format `JJJJ-MM-TT.N`), sonst übernimmt die App die Änderung nicht.
- Kurze Namen wie `Git` werden nur als ganzes Wort erkannt. Bei mehreren passenden Regeln gewinnt der längste Name.
- Keine persönlichen Daten, keine Werbung, keine Links zu inoffiziellen Downloads.
- Die Action „Daten prüfen“ kontrolliert jeden Pull Request. Ist sie rot, zeigt sie, was zu ändern ist.
- In `pending.json` gibt es neben `description` optional `description_en`.

Mit deinem Beitrag stimmst du zu, dass er unter [CC BY 4.0](LICENSE) veröffentlicht wird.

---

## English

Thank you for helping! Every rating helps people thinking about switching from Windows to Linux.

- **Easiest way:** in Linux Readiness Check, open “Rate programs” in the sidebar of the start screen, load the list and rate programs you have tried on Linux yourself. The app shows you exactly what is sent beforehand.
- **Issue:** open an issue with the template **“Programm bewerten / Rate a program”**. Only rate programs you have used on Linux yourself.
- **Pull request:** changes to `rules.json` are welcome. Please keep each pull request to a few programs and briefly explain where the assessment comes from. The rule format is shown above; `reason` is German, `reason_en` the English version. Increase `rules_version` after every change. The “Daten prüfen” check must pass.
- `readiness`: `green` = works, `yellow` = workaround, `red` = difficult.

By contributing you agree that your contribution is published under [CC BY 4.0](LICENSE).
