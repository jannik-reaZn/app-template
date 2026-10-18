export default {
  app: { title: "Haushaltsrechner" },
  common: {
    noExpenses: "Keine Ausgaben im gewählten Zeitraum.",
    payee: "Empfänger",
    category: "Kategorie",
    amount: "Betrag",
  },
  notFound: {
    title: "Seite nicht gefunden",
    message: "Die angeforderte Seite existiert nicht.",
    home: "Zur Startseite",
  },
  home: {
    summary: "{count} Ausgaben, insgesamt",
  },
  upload: {
    label: "CSV-Datei hierher ziehen",
    description: "oder zum Auswählen klicken (nur .csv)",
    errorTitle: "Datei konnte nicht geladen werden",
    loaded: "Geladen: {fileName}",
    privacy: "Die Daten bleiben nur im Browser und werden nicht gespeichert.",
  },
  range: { from: "Von", to: "Bis" },
  donut: { title: "Ausgaben nach Kategorie" },
  trend: {
    title: "Verlauf nach Kategorie",
    categories: "Kategorien",
    selectOne: "Bitte mindestens eine Kategorie auswählen.",
  },
  topPayees: {
    title: "Größte Empfänger",
    largestTitle: "Größte Einzelausgaben",
    date: "Datum",
    purpose: "Verwendungszweck",
  },
  comparison: {
    title: "Monatsvergleich",
    needTwoMonths: "Für einen Vergleich werden Ausgaben aus mindestens zwei Monaten benötigt.",
    month1: "Monat 1",
    month2: "Monat 2",
    difference: "Differenz:",
    noExpenses: "Keine Ausgaben in den gewählten Monaten.",
  },
  unmatched: {
    title: "Nicht zugeordnete Empfänger ({count})",
    info: "Diese Empfänger passen zu keinem Stichwort und landen in „{fallback}“. Die Zuordnung gilt für alle Buchungen des Empfängers, nur für diese Sitzung und über die ganze Datei. Für eine dauerhafte Zuordnung das Stichwort in data/mapping.json ergänzen.",
    bookings: "Buchungen",
    sum: "Summe",
    categoryFor: "Kategorie für {payee}",
  },
};
