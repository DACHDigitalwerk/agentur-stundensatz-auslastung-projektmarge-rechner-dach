# 📐 DACH Agentur-, Consulting- & IT-Dienstleister Stundensatz-, Auslastungs- (Billable Utilization) & Projektmarge-Rechner 2026

[![Live Web-App](https://img.shields.io/badge/Live_Web--App-Agentur_Stundensatz_&_Projektmarge_Rechner_2026-4f46e5?style=for-the-badge)](https://dachdigitalwerk.github.io/agentur-stundensatz-auslastung-projektmarge-rechner/)

Open-Source Python-Engine & interaktiver Online-Rechner für **Vollkosten- & Ziel-Stundensätze**, **Billable Utilization (fakturierbare Auslastung)**, **Overhead-Umlage pro Kopf**, **Künstlersozialabgabe DE (`5,0 %` KSK nach `§ 24 KSVG`)**, mehrstufige **Projekt-Deckungsbeitragsrechnung (`DB I`, `DB II`, `DB III`)** sowie **Festpreis-Scope-Creep-Risikopuffer** für Deutschland (`DE`), Österreich (`AT`) und die Schweiz (`CH`).

👉 **[Direkt zum interaktiven DACH Agentur-Stundensatz-, Auslastungs- & Projektmarge-Rechner 2026](https://dachdigitalwerk.github.io/agentur-stundensatz-auslastung-projektmarge-rechner/)**

---

## Kernformeln

- **Vollkosten-Stundensatz:**
  `Vollkosten_Stundensatz = (Jahresbruttogehalt * AG_Lohnnebenkostenfaktor + Overhead_pro_Kopf) / (Netto_Arbeitstage * Tagesstunden * Fakturierbare_Auslastung)`
- **Ziel-Stundensatz & Tagessatz:**
  `Ziel_Stundensatz = Vollkosten_Stundensatz / (1 - Ziel_EBIT_Marge)`
- **Projekt-Deckungsbeitrag (DB I → DB II → DB III) inkl. KSK (`5,0 %` in DE) & Scope-Creep:**
  - `DB I (AGI)` = `Projektumsatz - Externe_Freelancer - KSK_5_Prozent - Lizenzen`
  - `DB II` = `DB I - (Reale_Projektstunden * Direkter_Personalkosten_Stundensatz)`
  - `DB III (Projekt-EBIT)` = `DB II - (Reale_Projektstunden * Overhead_Stundensatz)`

## Schnellstart

```bash
pip install -e .
pytest -v
dach-agentur-marge --country DE --salary 72000 --utilization 70 --hours 180 --rate 125
```

## Rechtlicher Hinweis

Regelbasiertes mathematisch-schematisches Kalkulationswerkzeug gem. BGH, Urteil v. 09.09.2021 – Az. I ZR 226/20 (Smartlaw). Keine individuelle Rechts-, Sozialversicherungs- oder Steuerberatung i.S.d. § 2 RDG / § 5 StBerG.
