# Mitmachen

Danke, dass du helfen möchtest! Jede Bewertung hilft Menschen, die über einen Umstieg von Windows auf Linux nachdenken.

## Der einfachste Weg: in der App bewerten

In Linux Readiness Check unten auf dem Startbildschirm „Programme bewerten“ öffnen, die Liste laden und Programme bewerten, die du unter Linux selbst ausprobiert hast. Die App zeigt dir vor dem Senden genau, was gesendet wird.

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

Mit deinem Beitrag stimmst du zu, dass er unter [CC BY 4.0](LICENSE) veröffentlicht wird.
