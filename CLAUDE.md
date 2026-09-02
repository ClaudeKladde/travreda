# CLAUDE.md — Travreda

Projektinstruktioner för fortsatt utveckling. Läs hela filen innan du börjar.

---

## 1. Om projektet

**Travreda** är en tillgänglighetsanpassad webbapp för att bygga reducerade
travsystem (SK ABC-reducering) för ATG:s spelformer — **V85, V75, V86, GS75,
V64, V5**, i första hand V85 — byggd specifikt för skärmläsaranvändare
(VoiceOver på iPhone i första hand).

- **Användare:** Claudio. Skärmläsaranvändare.
- **Konversationsspråk:** svenska. Gränssnittet är bara på svenska (ingen
  engelsk version, till skillnad från VO Turf List).
- **Leverans:** en enda fil, `index.html`, som publiceras via GitHub Pages.
  Repot är publikt (krävs för att GitHub Pages ska fungera på ett gratiskonto
  — repo-synlighet skyddar inte den publicerade sidan, bara källkoden, och på
  Free-planen kan Pages inte alls användas med ett privat repo).
- **Stödfiler utanför appen:** en GitHub Action (`.github/workflows/`) som
  hämtar dagens/kommande V85/V75/V86-omgångar från ATG åt oss, samt en liten
  genererad `data/games.json` som `index.html` läser. Detta räknas inte som
  ett avsteg från enfils-principen — det är infrastruktur, inte appkod.
- **Inga byggverktyg för själva appen.** Ren HTML + CSS + JS i `index.html`.

---

## 2. Arbetssätt — samma regler som VO Turf List

### Diskutera alltid först, bygg sedan

**Skriv ALDRIG kod förrän användaren uttryckligen bekräftat.**

1. Användaren beskriver vad han vill
2. Undersök koden/API:et och bekräfta hur det faktiskt fungerar idag
3. Sammanfatta exakt vad som ska ändras, ställ följdfrågor vid oklarheter —
   **en fråga i taget**, inte flera på en gång
4. Användaren säger uttryckligen "ja", "nu kör vi" eller liknande
5. **Först då** bygger du

### Undersök innan du påstår

Gissa aldrig om hur ATG:s API eller filformat fungerar. Flera antaganden i det
här projektet har visat sig fel vid närmare undersökning (se avsnitt 5–6) —
lita på verifierad data (API-svar, riktiga schemafiler, riktiga exempel),
inte på sekundärkällor eller dokumentation som kan vara inaktuell.

### Var ärlig om begränsningar

Om något är overifierat (t.ex. "ej testat med riktig GPS/riktig inlämning
ännu") — säg det rakt ut i koden/kommentarer och till användaren, istället för
att låtsas att det är bekräftat.

---

## 3. Obligatoriskt vid varje bygge

Längst ner i `index.html` finns:

```html
<span class="update-line">Vibe kodad med Claude av Travkladde, senast uppdaterad ÅÅÅÅ-MM-DD HH:MM</span>
```

Uppdatera alltid till aktuellt datum/klockslag vid varje nytt bygge.

Verifiera JS-syntax (`node --check`) och HTML-taggbalans innan du presenterar
resultatet, samma princip som VO Turf List. Detta gäller **alltid**, oavsett
ändringens storlek — det tar sekunder och fångar trasig kod.

**Full test i webbläsare (Playwright, med riktig eller mockad ATG-data)
bara vid nya funktioner eller strukturella ändringar** — ny vy, ny
beräkningslogik, ändrad DOM-uppbyggnad/event-koppling, nytt exportformat.
Ren text-/ordningsjustering (t.ex. flytta ett fält, ändra en formulering,
lägga till/ta bort ord i en uppläst mening) behöver bara syntaxkollen ovan
plus en genomläsning av koden — inte en full klick-igenom-testkörning.
Skulle du vara osäker på om en ändring är "bara text" eller faktiskt
strukturell, fråga användaren istället för att anta.

---

## 4. Tillgänglighet — samma princip som VO Turf List

Detta är en app för skärmläsaranvändare. Samma lärdomar gäller rakt av:

- **Undvik ARIA-brus.** Semantisk HTML först (`<h2>`, `<ul>`/`<li>`,
  `<select>`, `<button>`) — lägg bara till ARIA när HTML inte räcker.
  Ingen `role="toolbar"` (dubbeluppläsning), inget `role="list"` på `<ul>`.
- **Uppläsningsordning:** viktig info direkt efter namnet, i den ordning
  användaren bad om: **häst, kusk, tränare, procent, barfota** — inte i
  slutet av en lång mening.
- **Barfota visas alltid, precis som vagn** (`shoesInfo()`) — ändrat på
  uttrycklig begäran från en tidigare princip om att bara nämna barfota
  när hästen faktiskt går barfota. Visar nu "Skor på" som grundläge, exakt
  samma mönster som `sulkyMainRowText()`: ett prefix ("Skobyte ") läggs
  bara till om skorna faktiskt bytts sedan senast (`s.front.changed`/
  `s.back.changed`), oavsett om bytet ledde till barfota eller till skor
  på igen.
- **Fokushantering:** flytta fokus till avdelningens rubrik
  (`tabindex="-1"`) när man byter avdelning, så VoiceOver-användare inte
  tappar sammanhanget.
- **Standardkontroller:** `<select>` eller stegvisa knappar för bokstavsval
  (Ej vald/A/B/C/D) i normalläge (valbart, se "Bokstavsval: knappar eller
  meny" i avsnitt 7), en togg-knapp (`aria-pressed`) i "Vanligt
  system"-läget — robust med VoiceOver utan extra ARIA utöver
  `aria-pressed`.
- **Mörkt och ljust läge**, tydliga kontraster (se "Färgpalett" nedan),
  orange accentfärg för visuellt markerade/valda hästar samt för
  vagnbyten/skobyte/barfota i hästkortens textrad.
- Inga emoji i gränssnittet.

### Färgpalett — Växjö Lakers-inspirerad, ljust + mörkt tema

**Ersatte en tidigare ATG-inspirerad palett** (blå/gul) på uttrycklig
begäran — användaren ville istället ha sitt favoritlags (Växjö Lakers HC)
profilfärger: mörkblå och orange. **Färgerna hämtades och verifierades
mot en oberoende källa** (teamcolorcodes.com, vanligt citerad referens för
lagfärger), inte gissade: `#013A80` (mörkblå) och `#F37835` (orange).
Ersatte den tidigare gula CTA-färgen helt — inte ett tillägg vid sidan av,
utan en fullständig omfärgning av hela paletten, på uttrycklig begäran
("ersätt helt med Lakers-färger").

**Två teman, inte ett** — byggd efter uttrycklig begäran om ett ljust läge
som komplement till det mörka. Alla färgtokens är CSS custom properties på
`:root`, satta om under två villkor:

```css
:root{ /* mörkt tema, grundläge */ }
@media (prefers-color-scheme: light){
  :root:not([data-theme="dark"]){ /* ljust tema, om systemet föredrar ljust
    OCH inget manuellt val tvingar mörkt */ }
}
:root[data-theme="light"]{ /* ljust tema, manuellt tvingat */ }
```

`data-theme`-attributet sätts av `applyTheme()` baserat på `themeMode`
(`"auto"`/`"light"`/`"dark"`, sparas i `travreda-theme`) — **Auto** tar
bort attributet helt (då avgör `prefers-color-scheme` via media queryn),
**Ljust**/**Mörkt** sätter attributet explicit och vinner alltid över
systeminställningen. **En liten synkron `<script>`-snutt i `<head>`**
(före `<style>` stängs, före `<body>` ritas) läser `travreda-theme` och
sätter `data-theme` innan sidan hinner måla ut något — annars hade ett
manuellt valt tema (som skiljer sig från systemets) blinkat till fel färg
en bråkdel av en sekund vid varje sidladdning. Den stora `<script>`-blocket
längst ner i `<body>` har sin egen kopia av samma logik (`applyTheme()`)
som bara styr Inställningar-radioknapparna och tillämpar ändringar efter
sidladdning — de två skriptblocken gör alltså delvis samma sak medvetet,
av just det skälet.

**Kontrastvärden** (WCAG:s relativ-luminans-formel, inte uppskattade) och
varför två separata "orange"-tokens behövs:

- **`--accent` (`#F37835`, ren Lakers-orange):** används **bara som
  bakgrundsfyllnad** ihop med `--accent-fg` (nästan svart, `#1a0f00`) —
  t.ex. `.btn-primary`, aktiv avdelningsflik. Fungerar utmärkt som fyllnad
  i båda teman eftersom den då aldrig jämförs mot sidans bakgrund, bara
  mot sin egen ihopparade textfärg (7,6:1).
- **`--accent-text`:** en **separat, temaanpassad** ton för när orange
  behövs som text/kant direkt mot sidans bakgrund (t.ex. `.selected-label`,
  `.horse-row.marked`s kant). Ren `--accent` mot en ljus bakgrund ger bara
  2,5:1 — otillräckligt (WCAG kräver 4,5:1 för text, 3:1 för UI-kanter).
  Mörkt tema: samma klara orange (`#F37835`, 6,7:1). Ljust tema: en mörkare
  bränd orange (`#9c4a17`, 5,7:1) — samma nyans i grunden, bara mörkad för
  att fungera mot en ljus bakgrund.
- **`--brand-blue`** (marinblå, sekundäraccent — knappar, `<h2>`-kant,
  `.summary-box`-kant): mörkt tema använder en **ljusare** ton (`#2568b5`,
  3,3:1 mot den mörka bakgrunden — den äkta Lakers-marinblå `#013A80` hade
  bara gett 1,7:1 och nästan försvunnit mot en mörk sida). Ljust tema
  använder den äkta, mörkare `#013A80` rakt av (10:1 mot den ljusa
  bakgrunden, ingen ljusning behövs där). Vit text ovanpå ger utmärkt
  kontrast i båda teman (6,4/11:1).
- **`--danger`** (röd, struken/fel): mörkt tema oförändrad (`#ff8080`,
  7,7:1). Ljust tema egen, mörkare röd (`#a4161a`, 7,1:1) — den ljusa
  rosaröda hade varit näst intill oläslig mot en ljus bakgrund.
- **`--input-bg`/`--badge-bg`/`--detail-bg`/`--marked-bg`:** fyra
  ytterligare tokens som ersatte tidigare hårdkodade hex-värden (`#242424`,
  `#2a2a2a`, `#191919`, `#2a2410`) som bara fanns definierade för det mörka
  temat — måste bli temavariabler för att ljusa temat inte skulle ärva
  mörka, ologiska ytor. `--marked-bg` (bakgrunden på en bokstavsmärkt
  hästrad) är dessutom omfärgad från en gul till en orange ton för att
  matcha den nya accentfärgen.
- **`--stepper-bg`** (`#a34d1a`, samma värde i båda teman): en egen,
  mörkare orange ton för bokstavsstegrarens knappar (se "Bokstavsval:
  knappar eller meny" i avsnitt 7) — skild från både `--accent` (ljusare,
  CTA-knappar) och `--brand-blue` (marinblå, standardknappar), på
  uttrycklig begäran om att de ska synas tydligare bredvid hästkortets
  egen knapp. Vit text ger 5,8:1, gott och väl över 4,5:1. Återanvänds även
  på togg-knappen i Vanligt matematiskt system-läge ("Vald"/"Ej vald",
  `.toggle-select-btn`), på uttrycklig begäran — samma handling
  (välja/avmarkera en häst) som bokstavsstegrarens förstagångsval, så
  samma färg.

**Ytterligare knappdifferentiering** (på uttrycklig begäran, "större
skillnad mellan olika knappar"), två nya tokens, samma värden i båda
teman (medvetet inte temaanpassade som `--brand-blue` — dessa är rena
kontrastknappar mot sin egen kant/fyllnad, inte mot sidans bakgrund):

- **`--horse-btn-bg`/`--horse-btn-border`/`--horse-btn-fg`** på
  `.horse-row .horse-toggle` — bara hästkortens egna knappar, inte t.ex.
  `#avd-heading` som återanvänder samma `.horse-toggle`-klass för sitt
  utseende (skiljs åt med `.horse-row`-föräldraselektorn). **Mörkt tema:**
  mörk marinblå fyllnad (`#012a5e`, mörkare än standardknapparnas
  `--brand-blue`) + ljus blå kant (`#cddcee`) + vit text. Fyllnaden själv
  ger bara 1,7:1 mot den mörka sidbakgrunden — otillräckligt på egen hand,
  men den tydliga ljusa kanten (7,9:1 mot fyllnaden) är det som faktiskt
  avgränsar knappen visuellt, inte fyllnaden mot sidan.
  **Ljust tema — omvänt schema, fixad bugg:** samma mörka marinblå
  fyllnad som mörkt tema visade sig upplevas som "alldeles för mörk" mot
  den ljusa sidbakgrunden. Bytt till ljus blåton (`#d6e3f5`) + mörk
  marinblå kant (`#013A80`, samma ton som ljusa temats `--brand-blue`) +
  mörk marinblå text (`#012a5e`, 10,8:1) — samma idé som mörkt tema fast
  spegelvänd (ljus fyllnad, mörk kant/text istället för mörk fyllnad, ljus
  kant/text). Alla underelement (muted text 6,8:1, `--accent-text` 4,8:1,
  `--danger` 6:1) verifierade läsbara mot den nya ljusa fyllnaden.
- **`--tab-bg`** (`#7d6836`, en mörkad, Lakers-inspirerad "tan"-ton — det
  fjärde färgen i lagets profil utöver marinblå/orange/vitt, tidigare
  oanvänd) på avdelningsflikarna (`.avd-tab`, ej vald), skild från både
  hästknapparnas marinblå och den aktiva flikens orange. Den rena,
  ljusare Lakers-tan (`#B39759`) gav bara 2,6:1 mot ljusa temats bakgrund
  och 2,8:1 för vit text — mörkad för att fungera som knappfyllnad i båda
  teman (vit text 5,4:1, 3,5–4,9:1 mot bakgrunden i respektive tema).

**Alla knappar fick en tydlig bakgrundsfärg** (`--brand-blue`, vit text),
på uttrycklig begäran — tidigare hade bara `.btn-primary`
(gul/nu-orange) och några enstaka knappar en färgad bakgrund, resten var
platt mörkgrå. Formulärfält (`select`/`input`) fick en egen
`--input-bg`-ton istället, så de inte ser ut som knappar.
`#btn-open-atg`s tidigare egna specialstyling (från ATG-paletten) togs
bort som överflödig — alla knappar är redan marinblå nu.

**Menyknappen flyttad till allra överst på sidan** (`.menu-wrap`, nu
första elementet i `#view-avdelning`, före `#avd-progress`), på uttrycklig
begäran ("flytta upp menyknappen längre upp i det högra hörnet") — var
tidigare `position:absolute` inuti den sticky menyraden tillsammans med
avdelningsflikarna. `.avd-tabs`s `padding-right:3.6rem` (som reserverade
plats åt den gamla positioneringen) togs bort som överflödig.

**Skalning/zoom:** hela stilmallen gicks igenom rad för rad (samma
genomgång som tidigare, fortfarande giltig efter omfärgningen). Praktiskt
taget allt är redan `rem`-baserat — enda `px`-förekomsterna är
hårlinje-kantlinjer/`border-radius` (som inte behöver skala enligt WCAG)
och den avsiktliga 1×1px-tekniken i `.visually-hidden`. `viewport`-taggen
saknar `maximum-scale`/`user-scalable=no`, så pinch-zoom är aldrig
blockerad.

**Ny inställning "Tema"** (`themeMode`) under Inställningar, tre
radioknappar (Följ systemets inställning/Ljust/Mörkt), samma mönster som
Sortering/Komprimering/Bokstavsval. "Följ systemets inställning" är
förvalt.

### Hästkortens struktur (avdelningsvyn)

Varje häst är en `<h3>` som **omsluter** den enda knappen
(`<h3><button class="horse-toggle">...</button></h3>`) — inte en syskon-
rubrik bredvid knappen. Testat och bekräftat att detta ger exakt **ett**
svep/tabbstopp per häst (plus ett till för bokstavsvalet/kryssrutan) i
både VoiceOver-svep och Tab-navigering på dator, samtidigt som rubriken
fortfarande går att nå via rotorns rubriknavigering — en h3 som bara
innehåller en knapp är ett vanligt, giltigt mönster (samma som "kort med
klickbar rubrik" överallt på webben). En tidigare version hade `<h3>` och
knappen som syskon, vilket dubblerade antalet svep per häst — rättat.

- Knappens innehåll, i uppläsningsordning: statusetikett **först** ("Struken."
  eller "Vald A-häst."/"Vald." i Vanligt system-läge — bara en kan gälla
  samtidigt), sedan nummer+namn+procent (`.horse-top`, samma rad
  visuellt), sedan kusk/tränare, vagn, barfota. Statusetiketten uppdateras
  live vid varje bokstavs-/kryssruteändring (`updateSelectionLabel()`).
- **Kommaseparerad, inte punktseparerad** huvudrad, på uttrycklig begäran
  (kortare paus mellan delarna i talsyntesen): `"5 Mellby Narrow, 33.4%,
  Daniel Wäjersten, Daniel Wäjersten, Vanlig vagn, Barfota runt om."` — bara
  den allra sista delen (vagn eller barfota, beroende på vilka som finns)
  avslutas med punkt. Byggs av en array (`subParts`) i renderingen istället
  för att varje del bakar in sitt eget skiljetecken, eftersom vilken del som
  är sist varierar (vagn/barfota kan saknas). "Kusk:"/"Tränare:"-etiketterna
  är borttagna från huvudraden (bara namnen) — etiketterna finns kvar i
  detaljvyn.
- **Vagnbyte/skobyte som prefix, inte suffix.** Var tidigare `"Vagn: X,
  vagnbyte."` respektive en parentetisk `"(barfota för första gången)"` sist
  i meningen — båda flyttade till ett prefix istället, konsekvent med
  varandra: `"Vagnbyte Amerikansk vagn"` / `"Skobyte Barfota runt om"`.
  `sulkyMainInfo()`/`shoesInfo()` returnerar numera `{text, highlight}`
  istället för en ren sträng — huvudradens `subParts`-array lägger till
  rätt avslutande skiljetecken beroende på position, precis som förut.
- **Färgmarkering av vagnbyten/skoinfo** (`--accent-text`, samma
  orange-ton som resten av accentfärgen), på uttrycklig begäran om
  tydligare visuell indikering. `highlight` är sant för vagn bara vid ett
  faktiskt byte (`s.type.changed`) — en oförändrad "Vanlig vagn" är inte
  märkvärdig nog att markera. För skor är `highlight` sant både vid byte
  **och** vid barfota (även utan byte) — barfota i sig är relevant
  spelinformation, inte bara själva bytet. Byggs med egna `<span
  class="changed-info">`-element runt bara den delen av raden istället för
  `addSub()`s enda textnod, eftersom bara en del av `.horse-sub` ska få
  färgen.
- **Minimera-knapp:** när detaljvyn expanderas läggs en "Minimera
  {namn}"-knapp till sist i detaljinnehållet, så att man landar på en
  tydlig stängknapp efter att ha svept igenom all information, istället för
  att behöva svepa bakåt till den ursprungliga knappen.
- **Minimera-knapp:** när detaljvyn expanderas läggs en "Minimera
  {namn}"-knapp till sist i detaljinnehållet, så att man landar på en
  tydlig stängknapp efter att ha svept igenom all information, istället för
  att behöva svepa bakåt till den ursprungliga knappen.

### Detaljvyns rader + valbara fält

Den utfällda detaljvyn (tidigare ett enda sammanhängande stycke, sedan
grupperad i fyra stycken) är nu uppdelad i **en `<p>` per rad** — en
`<ul>`-liknande gruppering utan extra ARIA, byggd av `buildDetailLines()`.
Varje rad motsvarar exakt en kryssruta under Inställningar (`DETAIL_FIELDS`,
se nedan), på uttrycklig begäran: "detta blir tydligare enligt kryssrutorna
i inställningarna" — en VoiceOver-användare svepar alltså förbi en rad i
taget, inte en hel grupp. Grundordningen är, i tur och ordning: Trendprocent,
säsongsstatistik, intjänade pengar, startpoäng, rekord, hemmabana, Tränare,
Kusk, Odds (häst → tränare → kusk var uttryckligen efterfrågad tidigare,
oförändrat) — men ordningen är numera **omsorterbar**, se "Ordning på
raderna" nedan. En rad utan data eller vars kryssruta är avstängd renderas
inte alls — samma "hellre tyst än tomt element"-princip som resten av
appen.

**Förkortad text, på uttrycklig begäran** ("ta bort en del överflödiga
ord"): `"Trendprocent: +2,2 procentenheter."` → `"Trend +2,2%."`,
`"Pengar: X kr intjänat totalt."` → `"Pengar: X kr."`, `"Bästa rekord:"` →
`"Rekord:"`. Kusk/tränare-procenten (`winStatsText()`) skriver nu ut
decimaltecknet med komma och utan mellanslag före procenttecknet
(`"27,2% (...)"`, inte `"27.2 % (...)"`) — konsekvent med resten av appens
talformat.

**Ålder/kön/färg, vagn (detaljraden), ägare och uppfödare är borttagna helt**
från detaljvyn, på uttrycklig begäran — inte bara avstängda. Vagnens
huvuduppgift finns kvar på hästens huvudrad (`sulkyMainRowText`) som förut,
bara detaljradens mer utförliga variant (färg, bytesmarkering) är borta.
`sulkyDetailText()` och `SEX_TEXT` togs bort som död kod eftersom de bara
användes av de borttagna raderna.

**Två nya fält, hittade i data som redan hämtas men aldrig använts:**

- **Trendprocent** (`pools[TYP].trend`, per häst) — hur spelprocenten
  förändras just nu. **Inte dokumenterad av ATG** (hittades bara genom att
  inspektera ett riktigt API-svar), så tolkningen av enheten (`trend × 100`
  som procentenheter) är en rimlig gissning, inte bekräftad. Ett värde som
  avrundar till 0,0 tappar sitt +/−-tecken (annars kunde det bli det
  missvisande "-0,0 procentenheter").
- **Intjänade pengar** (`horse.money`, redan i kronor — samma tal som
  `statistics.life.earnings` fast redan delat med 100) — hästens totala
  livstidsintjäning, formaterat med `toLocaleString("sv-SE")` för
  tusentalsavgränsare.

**Ett tredje fält, tillagt senare** efter en direkt fråga om det fanns —
**Startpoäng** (`horse.statistics.life.startPoints`, ett heltal, t.ex.
`4750`) — verifierat i riktig data, ingen extra hämtning behövs. Visas som
`"Startpoäng: 4750."`, i grundordningen direkt efter Pengar-raden (på
uttrycklig begäran).

**Total omsättning** för hela omgången (`currentGame.pools[TYP].turnover`,
från spelets toppnivå-`pools`-objekt — måste sparas explicit på
`currentGame` i `loadGame()`, fanns inte där tidigare) visas i en egen rad,
**`#avd-turnover`**, direkt under `#avd-progress` (omgångens namn) — en
egen `<p>` och därmed ett eget svep, inte sammanslagen med namn-raden.
Döljs helt (`hidden`) om omsättning saknas i svaret. Avrundad till hela
kronor: `"Omsättning: 6 507 253 kr."`

**Valbara fält:** en kryssrutegrupp under Inställningar (`DETAIL_FIELDS`,
en post per kvarvarande rad ovan plus Tränare/Kusk/Odds som egna
kryssrutor — nio totalt) låter användaren stänga av enskilda rader.
Sparas i `travreda-detail-fields` (ett objekt `{nyckel: boolean}` i
localStorage), alla på som standard.

**Ordning på raderna:** varje rad under Inställningar har numera två
knappar, **"Flytta upp"/"Flytta ner"** (`aria-label` med fältnamnet
inbakat, t.ex. "Flytta upp Startpoäng", eftersom "Flytta upp" upprepat på
flera rader annars är tvetydigt för en skärmläsare) — byggt efter
uttrycklig begäran, valt istället för drag-and-drop som är svårare att
använda med VoiceOver. Första radens "Flytta upp" och sista radens "Flytta
ner" är **inaktiverade, inte dolda** (`disabled`, inte `hidden`) eftersom
det inte finns någonstans att flytta till.

Ordningen ligger i en egen array, `detailFieldOrder`, separat från
`detailFields` (som bara styr av/på) och sparas i en egen
localStorage-nyckel, `travreda-detail-field-order`. **`buildDetailLines()`**
byggdes om från en hårdkodad if-kedja i fast ordning till att loopa genom
`detailFieldOrder` och slå upp varje fälts textbyggare i en ny
`DETAIL_FIELD_BUILDERS`-tabell (en funktion per fältnyckel, samma logik som
innan — bara flyttad in i tabellen) — så att den ordning som faktiskt
byggs och läses upp alltid matchar exakt vad Inställningar visar, med noll
risk att de två divergerar.

**Migrering:** en sparad ordning läses bara in om den är en giltig
**permutation** av alla kända fältnycklar (samma antal, inga dubbletter,
inga saknade) — annars faller den tillbaka på grundordningen. Detta löser
automatiskt introduktionen av det nya Startpoäng-fältet: en användare med
en gammal sparad ordning (från innan fältet fanns) får grundordningen
igen (som redan har Startpoäng på rätt plats) istället för att fältet
saknas eller kraschar något.

### Sticky avdelningsflikar + meny

Flikstorleken (`.avd-tab`, `2,2 rem` + `.45rem` mellanrum — höjd från
`1,9rem`/`.3rem` på uttrycklig begäran om "något större och med mera luft
mellan") är avpassad för att rymma alla 8 avdelningar på en rad ner till
~375px skärmbredd (iPhone SE och uppåt). Vid det ovanligare, smalare
320px-läget (äldre iPhone SE 1:a gen) radbryts flikarna till två rader
istället — `flex-wrap:wrap` hanterar detta automatiskt utan att något
går sönder, en medveten avvägning eftersom 320px är ett allt ovanligare
skärmbredd. **Den aktiva fliken** har en egen, mer mättad orange ton
(`--tab-active-bg`, `#e8590c`) istället för den delade `--accent`
(`#F37835`, används av CTA-knappar/menyknappen) — på uttrycklig begäran
om "starkare färg", för att den markerade avdelningen ska sticka ut
ännu tydligare bland de andra flikarna.

**Menyknappen är flyttad ur den sticky menyraden helt** (på uttrycklig
begäran, "flytta upp menyknappen längre upp i det högra hörnet") — ligger
nu som **allra första elementet** i `#view-avdelning`, före `#avd-progress`.
`.menu-wrap` gick från `position:absolute` (förankrad i den sticky radens
positioneringskontext) till ett vanligt block-element (`position:relative`,
`display:flex;justify-content:flex-end`) som själv utgör
positioneringskontexten för `#main-menu`-dropdownen. `.avd-tabs`s gamla
`padding-right:3.6rem` (som reserverade plats åt menyknappen i den
tidigare positioneringen) togs bort som överflödig. **`#btn-menu-toggle`**
fick dessutom en egen orange bakgrund (`--accent`/`--accent-fg`, samma
par som `.btn-primary`) istället för standardknapparnas marinblå, på
uttrycklig begäran om att den ska synas ännu bättre.

**Sidhuvudets ordning på huvudsidan** (`view-avdelning`): `.menu-wrap` →
`#avd-progress` (omgångens namn: "V85 — Romme — 2026-08-22") →
`#avd-turnover` (omsättning) → `.topbar` (nu bara avdelningsflikarna,
fortfarande sticky) → `avd-heading` (lopprubrik) → `avd-terms` (se nedan)
→ `avd-marked-count` → hästlistan.

**`#avd-terms`** (direkt efter lopprubriken `avd-heading`) visar loppets
deltagandevillkor — ålder, kön, intjänandegränser, körsvenskrav — direkt
från ATG:s egen `race.terms`-array (redan hämtad, inga extra anrop),
sammanslagen till en löpande text (`formatTermsText()`).

**Hela lopprubriken är knappen** (byggd efter uttrycklig begäran, samma
mönster som hästkortens `<h3><button>...</button></h3>` — en `<h2>` som
bara omsluter en enda knapp, `id="avd-heading"`) — ett tryck
visar/döljer `#avd-terms` (`aria-expanded`/`aria-controls`, samma
öppna/stäng-princip som "Tips och instruktioner"-knappen på Startsidan).
Innehållet är dolt som standard och **återställs till dolt varje gång**
`renderAvdelning()` körs (byte av avdelningsflik, ny omgång) — inte
kvarhållet expanderat mellan olika lopp. Klick-hanteraren sätts upp en
enda gång vid sidladdning (inte inuti `renderAvdelning()`, som körs vid
varje flikbyte — annars hade lyssnare staplats på varandra); saknar loppet
`terms` gör ett klick ingenting (`avdTermsEl.textContent` är tomt).
`class="horse-toggle"` återanvänds för utseendet (samma fullbredds-knapp
utan extra CSS behövs).

**`formatTermsText()`** skriver om två saker i ATG:s annars redan
färdigformulerade text, verifierat mot riktiga API-svar (Romme 2026-08-22
och en GS75-omgång), efter uttrycklig begäran om tydligare uppläsning:

- **Datum:** ATG skriver födelsedatum som en rå sexsiffrig sträng utan
  separatorer (`"Körsvenner födda 080822 eller tidigare."`,
  DDMMÅÅ) — en talsyntes läser lätt detta som ett stort tal istället för
  ett datum. `expandCompactDate()` skriver om till `"8 augusti 2022"`.
  Samma mönster förekommer även efter `"fr.o.m."` i vissa lopp (t.ex.
  B-träningsvillkor) — båda hanteras av samma regex
  (`/(födda|fr\.o\.m\.) (\d{6})/g`). **Antar 2000-talet** för det
  tvåsiffriga året (`2000 + åå`) — inte verifierat mot ett fall där detta
  skulle vara fel, men rimligt så länge ATG:s texter bara handlar om
  nutida datum.
- **Beloppsintervall:** bindestrecket i `"300.001 - 1.950.000 kr"` skrivs
  om till `"300.001 till 1.950.000 kr"` — ett fristående bindestreck
  riskerar att läsas som "minus" eller hoppas över helt av en skärmläsare.
  Träffar bara siffra-mellanslag-bindestreck-mellanslag-siffra-kr
  (`/(\d[\d.]*)\s-\s(\d[\d.]*\s*kr)/g`), inte t.ex. `"3-åriga"` (inget
  mellanslag runt bindestrecket där).

Döljs helt om loppet saknar `terms`.

---

## 5. ATG:s API — vad vi vet, verifierat

### Endpoints

```
https://www.atg.se/services/racinginfo/v1/api/calendar/day/{datum}   CORS-låst till atg.se, används bara server-sidan (GitHub Action)
https://www.atg.se/services/racinginfo/v1/api/games/{spel-id}        CORS ÖPPEN (Access-Control-Allow-Origin: *) — kan hämtas direkt från index.html
https://www.atg.se/services/racinginfo/v1/api/races/{lopp-id}        CORS-låst till atg.se, används inte
```

**Spel-id-format:** `{TYP}_{datum}_{bankod}_{första avdelningens loppnummer}`,
t.ex. `V85_2026-08-22_23_5` (Romme = bankod 23). Bankoden och avdelningarnas
loppnummer finns redan i `/games/{id}`-svaret (`race.track.id`/`.name`), så
ingen separat hårdkodad bankodstabell behövs när vi väl har ett spel-id.

**Fixad bugg — fel bankod i exportfilen gav "Angivet spel är inte
tillgängligt" hos ATG (två omgångar, tre försök, till slut rätt fixat):**
rapporterad av användaren efter en avvisad V86-inlämning, och sedan igen
efter ett andra, oberoende V86-tillfälle en vecka senare. Grundorsak:
**V86 körs numera alltid över två olika banor** (Solvalla + en av
Åby/Jägersro/Bergsåker, varje vecka) — de två rapporterade fallen
(`V86_2026-08-26_40_1`: Åby/Solvalla, `V86_2026-09-02_40_1`:
Solvalla/Axevalla) bekräftar båda mönstret.

Ett **första fixförsök** (efter det första fallet) antog att rätt bankod
för exporten var **avdelning 1:s fysiska bana** (`data.races[0].track.id`,
6/Åby) — bättre än den ursprungliga, ännu mer felaktiga gissningen
(`tracks[0]` ur kalenderns osorterade lista, 5/Solvalla), men **fortfarande
fel**: det andra, oberoende V86-fallet avvisades med exakt samma fel trots
korrekt ifylld avdelning-1-bana (8/Axevalla). Grundligt verifierat först då
den verkliga orsaken hittades:

- Spel-id:t för **båda** de rapporterade flerbanefallen innehöll bankoden
  **40** (`V86_2026-08-26_40_1`, `V86_2026-09-02_40_1`) — trots att de
  gällde helt olika banpar. 40 finns **inte** med i ATG:s egen officiella
  bankodslista över riktiga svenska travbanor.
- Källkoden till [HPTClient](https://github.com/Hospodaren/HPTClient) (det
  verkliga, i produktion beprövade referensverktyget, se avsnitt 6)
  innehåller en ATG-härledd bankodsenum där **bankod 40 = `ExtraE`** — en
  av flera reserverade specialkoder (`ExtraC`=20, `ExtraD`=30, `ExtraE`=40,
  `ExtraJ`=49), uttryckligen **undantagna** när samma källkod listar
  "riktiga svenska banor". Samma källkod refererar även ett
  `HostTrackId`-begrepp — en banidentitet för hela den kombinerade
  omgången, skild från de enskilda lopplatsernas fysiska banor.
- En **helt oberoende användare** på ett diskussionsforum (Flashback)
  rapporterade exakt samma symptom för V86-filinlämning och löste det,
  utan koppling till Travreda eller HPTClient, med `trackcode="40"`.

Tre oberoende källor pekar alltså samstämmigt på att bankoden för en
flerbaneomgång inte är någon fysisk bana alls, utan ATG:s reserverade
specialkod för hela den kombinerade omgången — och den koden råkar redan
finnas där, inbakad i spel-id:t självt.

**Den slutgiltiga fixen:** bankoden hämtas nu ur **spel-id:ts egen
inbäddade bankodskomponent** (`{TYP}_{datum}_{bankod}_{avdelning}`,
`id.split("_")[2]` i `loadGame()`, motsvarande parsning i
`scripts/fetch_games.py`) — inte ur någon hämtad lopp-data alls. För
enkelbanespel är detta exakt samma tal som avdelning 1:s fysiska bana
(ingen ändring i praktiken, t.ex. Romme = 23 i båda fallen), så fixen är
bakåtkompatibel. `scripts/fetch_games.py` slipper därmed också gissa eller
dölja bankoden vid flerbanespel — `trackId` sätts korrekt direkt från
kalenderns egen `game["id"]`-sträng, ingen extra `/games/{id}`-hämtning
behövs för detta.

Verifierat med Playwright mot riktig, levande data för
`V86_2026-09-02_40_1`: exportfilens `trackcode` blev `40` för samtliga
kuponger (tidigare felaktigt `8`), och en regressionstest mot ett
enkelbanespel (`V85_2026-08-22_23_5`, Romme) bekräftade oförändrat `23`.

**Den tidigare varningen i appen** (`#avd-multitrack-warning`, som jämförde
varje avdelnings bana mot avdelning 1:s bana och varnade om flerbanespel)
är **borttagen** på uttrycklig begäran — den byggdes för att kompensera
för den då okända risken med fel bankod, men fyller inget syfte nu när
bankoden alltid hämtas korrekt direkt ur spel-id:t, oavsett hur många
fysiska banor omgången spänner över.

**Andra, separata bugg-rapport med samma ATG-felmeddelande:** en efterföljande
inlämning (samma omgång, `V86_2026-08-26_40_1`, den här gången med **korrekt**
bankod `6` efter fixen ovan) avvisades ändå med exakt samma
"Angivet spel är inte tillgängligt". Verifierat via `curl` direkt mot
`/games/V86_2026-08-26_40_1` vid tidpunkten för felet: omgångens
`status`-fält (toppnivå i svaret) hade gått från `"bettable"` till
`"ongoing"` — de flesta avdelningarna visade redan `race.status:"results"`.
Orsaken var alltså helt orelaterad till bankodsbuggen: filen lämnades in
efter att omgången redan startat (avdelning 1:s starttid var 20:30, båda
inlämningsförsöken skedde efter det), och ATG accepterar bara filer för
omgångar som fortfarande är `"bettable"`.

**Fix — proaktiv kontroll i appen** (direkt uppföljning av användarens
ursprungliga begäran om att "bygga in en kontroll i verktyget"):
`loadGame()` sparar numera även `data.status` på `currentGame`. En ny
`GAME_STATUS_TEXT`-tabell (`bettable`/`ongoing`/`results`) mappar det till
en läsbar svensk fras. `renderAvdelning()` visar, precis som
flerbane-varningen, en egen röd varningsrad
(**`#avd-not-bettable-warning`**, direkt före `#avd-multitrack-warning`)
så fort `currentGame.status` finns och inte är `"bettable"` — texten
förklarar rakt av att en inlämning kommer avvisas. `renderLiveSummary()`
sätter dessutom `exportBtn.disabled=true` (och skriver över
`#calc-status` med en hänvisning till varningen högst upp) så fort
omgången inte är `bettable`, oavsett hur många rader systemet annars har
— **exportknappen ska aldrig gå att trycka på** för en omgång som inte
längre går att lämna in en fil för. Detta är ett rent klientsidigt,
tidsstämpelfritt tillståndstest (bara `currentGame.status` vid senaste
hämtning) — appen pollar inte kontinuerligt, så en omgång som startar
**medan** man sitter och fyller i systemet upptäcks först vid nästa
uppdatering/omladdning, inte i realtid.

Verifierat med Playwright mot en riktig, levande hämtning av samma
omgång efter att den gått till `"ongoing"`: varningsraden visade korrekt
"Omgången pågår redan hos ATG …", och exportknappen förblev inaktiverad
även efter att alla åtta avdelningar fått en markerad häst.

**Hastighetsgräns:** okänd exakt gräns för denna endpoint (till skillnad från
Turfs dokumenterade "1 anrop/sekund") — `index.html` gör bara ett anrop per
vald omgång, ingen polling, så det har inte varit ett problem hittills.

### Vad `/games/{id}` innehåller (per häst i `race.starts[]`)

- `horse.name`, `horse.shoes.front/back.hasShoe` (barfota, `false` = barfota)
  + `.changed` (skobyte)
- `horse.trainer` / `driver` med namn och `statistics.years[år].winPercentage`
  (observera: delas med 100 för procent, t.ex. `1333` → 13,33 %)
- `pools.{TYP}.betDistribution` per häst = spelprocent × 100 (summerar till
  10000 per lopp), `pools.vinnare.odds` = odds × 100

### Hur vi hittar dagens/kommande omgångar

`/calendar/day/{datum}` är CORS-låst till atg.se — **fungerar inte** från en
webbläsare på GitHub Pages. Löst med en schemalagd GitHub Action
(`.github/workflows/fetch-games.yml` + `scripts/fetch_games.py`) som gör
anropet server-sidan (CORS gäller bara webbläsare) för kommande dagar, och
skriver en liten `data/games.json` som `index.html` läser via ett vanligt
`fetch()` (samma ursprung, GitHub Pages). Uppdateras några gånger om dagen.

Manuellt fallback i appen (om `games.json` saknar en omgång): mata in
datum + bankod + speltyp, appen provar spel-id med startavdelning 1–12 mot
den öppna `/games/{id}`-endpointen tills rätt omgång hittas — ren
klientsidig lösning, inget nytt serveranrop behövs.

**Egna rubriker per speltyp på Startsidan** (byggt efter uttrycklig
begäran) — `loadGamesList()` grupperar inte längre alla hämtade omgångar i
en enda lista, utan bygger en `<h3>{TYP}</h3>` + egen `<ul class="game-list">`
per speltyp, i en fast ordning (`GAME_TYPE_ORDER`): **V85, V86, V75, GS75,
V64, V5**. En speltyp utan några kommande omgångar får ingen rubrik alls
(döljs helt, inte en tom sektion) — samma "hellre tyst än onödigt
pratig"-princip som resten av appen. `#games-list` är numera en `<div>`
istället för en `<ul>` (måste kunna innehålla `<h3>`+`<ul>`-par, en ren
`<ul>` kan bara ha `<li>` som direkta barn).

Knapptexten under varje rubrik hade först speltypen borttagen helt (rubriken
sa det redan) — **återinförd på användarens begäran**, men i ett nytt
format: banan följt av speltypen (`"Solvalla, V86 — 2026-08-26 kl 18:00"`,
inte `"V86 — Solvalla — …"` som innan grupperingen). Motiveringen var att
göra det tydligt när samma bana har flera omgångar av olika speltyper
samma dag — bara rubriken räcker inte om man svepit förbi den och tappat
sammanhanget.

### Spelformer — V85, V75, V86, GS75, V64, V5

Utökat från de ursprungliga V85/V75/V86 efter uttrycklig begäran. Verifierat
mot det riktiga XSD-schemat (`atg_filebetting_1_8_6.xsd`, hittat i
HPTClient-källkoden, se avsnitt 6) och live mot ATG:s eget API, inte antaget:

| Typ | Avdelningar | `trackcode` i exporten? |
|---|---|---|
| V85 | 8 | Ja |
| V86 | 8 | Ja |
| V75 | 7 | **Nej** |
| GS75 | 7 | **Nej** |
| V64 | 6 | **Nej** |
| V5 | 5 | Ja |

`LEG_COUNT`/`COUPON_TAG`/`COUPON_HAS_TRACKCODE` styr detta generiskt per
speltyp — spel-id-formatet (`{TYP}_{datum}_{bankod}_{avdelning}`), brute
force-sökningen och `/games/{id}`-svarets struktur (pools/driver/tränare/
skor) är identiska för alla sex typerna, verifierat live mot riktiga
spel-id:n för samtliga.

**Galoppfiltrering:** till skillnad från V85/V75/V86 (alltid trav) kan
GS75/V64/V5 gå på **galoppbanor** — verifierat live (t.ex. `V64_2026-08-23
_79_4` på Övrevoll är galopp, samma dags GS75/V5 är trav). Travreda hanterar
bara travdata (inga fält för galoppens `blinders`/`jockey` etc.), så
`scripts/fetch_games.py` filtrerar **alla** speltyper (inte bara de tre
nya, som extra säkerhetsmarginal) på kalenderns egna `tracks[].sport`-fält
(`"trot"`/`"gallop"`) innan en omgång tas med i `data/games.json` — ingen
extra API-anrop behövs, fältet finns redan i samma `/calendar/day/{datum}`
-svar som `track_names` byggs från. Det manuella fallbacket i appen (mata
in datum/bankod/speltyp) har ingen motsvarande filtrering — en galoppomgång
går alltså tekniskt att ladda manuellt, men visar då tomma/felaktiga fält
eftersom `horse.shoes`/`start.driver` saknas i galoppdata. Medvetet
accepterad begränsning i den manuella vägen, inte byggd ännu.

**Bugg hittad och fixad i samband med detta:** exporten skrev tidigare ut
`trackcode`-attributet på **alla** kupongtyper, inklusive V75 — men enligt
schemat saknar `v75Coupon` (liksom det nya `gs75Coupon`/`v64Coupon`) det
attributet helt (flerbane-spel, inget enskilt spårnummer att ange). Ospårat
tidigare eftersom bara V85 testats mot en riktig filinlämning på atg.se.
`generateXml()` kollar nu `COUPON_HAS_TRACKCODE[game.type]` och utelämnar
attributet helt för de typer som saknar det.

---

## 6. Export till ATG (filinlämning) — verifierat

**Källa:** det verkliga XML-schemat (`atg_filebetting` version **1.8.6** —
inte 1.8.2/1.8.4 som är de enda versionerna som går att hitta direkt på
`atg.se/services/schemas/filebet/`; 1.8.6 hittades i källkoden till det
verkliga, i produktion beprövade verktyget
[HPTClient](https://github.com/Hospodaren/HPTClient), som visar exakt hur en
riktig ATG-fil för V85 byggs) plus ett verkligt exempel från Jokersystemet
(PDF-export av ett riktigt V85-system, Romme 2026-08-22).

**V85 saknas i de äldre schemaversionerna** (1.8.2/1.8.4) som går att hämta
direkt från atg.se idag — det är därför det såg ut som att V85 saknade
filstöd innan användaren rättade detta. `v85CouponType` finns i 1.8.6.

### XML-struktur

```xml
<?xml version="1.0" encoding="UTF-8"?>
<issuer xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="https://www.atg.se/services/schemas/filebet/1.8.6/atg_filebetting.xsd"
    company="Travreda" product="Travreda" version="1.0"
    createddate="ÅÅÅÅ-MM-DD" createdtime="HH:MM:SS"
    schemaversion="ATG File Betting XSD ver 1.8">
  <betcoupons>
    <v85Coupon couponid="1" date="ÅÅÅÅ-MM-DD" trackcode="23" betmultiplier="1">
      <leg legno="1" marks="000000100000000" />
      <!-- ... en leg per avdelning (8 för V85/V86, 7 för V75) ... -->
    </v85Coupon>
    <!-- en kupong per exporterad rad ELLER, vid komprimering, per bokstavsmönster
    (flera hästar markerade i marks på en och samma leg — se "Kupongkomprimering" nedan) -->
  </betcoupons>
</issuer>
```

`marks` = 15 tecken, position = startnummer, `1` = markerad (kan vara flera
`1`:or på en och samma leg, se komprimering nedan). `couponid` är löpnummer i
filen (1–9999 enligt schemat).

**v1 exporterade en `<coupon>` per godkänd rad (okomprimerat).** Riktig
kupongkomprimering är nu byggd, se "Kupongkomprimering" nedan.

**Reservhästar (r1/r2 i schemat, för stryknings-ersättning) hanteras inte i
v1** — medvetet vald begränsning, se konversationshistorik. Kuponger är
giltiga utan dem, bara utan automatisk ersättning vid strykning.

**Radpris varierar per speltyp** (`ROW_PRICE`) — **bugg rapporterad och
fixad:** appen antog tidigare 0,50 kr/rad för alla sex speltyper (kvar
sedan v1, innan V86/GS75/V64/V5 lades till). Fel: bara V85/V75 kostar
0,50 kr. Verifierat mot ATG:s egen kundtjänstguide ("Vilka spelformer
finns och hur högt är radpriset?"):

| Typ | Kr/rad |
|---|---|
| V85 | 0,50 |
| V75 | 0,50 |
| V86 | 0,25 |
| GS75 | 1 |
| V64 | 1 |
| V5 | 1 |

V85:s pris (0,50 kr) är dessutom bekräftat via ett oberoende verkligt
exempel (Jokersystemet-PDF:en: 1865 rader × 0,50 kr = exakt 932,50 kr) —
övriga fem typers pris vilar bara på kundtjänstguiden ovan, inte på ett
eget verkligt inlämnat exempel. Dubbelkolla alltid faktiskt pris på
atg.se innan du lämnar in en fil, speciellt för en ny speltyp.
`renderLiveSummary()` slår upp `ROW_PRICE[currentGame.type]` istället för
ett hårdkodat tal, och sammanfattningsraden anger numera vilket pris/rad
och vilken speltyp som använts (`"0,50 kr/rad för V85 — bekräfta alltid på
atg.se."`) istället för ett generiskt "0,50 kr/rad antaget" oavsett
speltyp.

**Testat mot en riktig filinlämning på atg.se** (2026-08-22, inför omgången
den 25:e) — filen gick att lämna in, men gav ett varningsmeddelande:
"Det verkar som om filen har ändrats sedan den tillverkades
(checksummefel) ... Det går bra att lämna in filen trots detta fel."

**Orsak och fix:** filnamnet måste innehålla en CRC16-checksumma av filens
eget innehåll, som ATG tydligen verifierar vid uppladdning. Detta hittades
i HPTClients källkod (`Crc16.cs`) — standard **CRC-16/ARC** (polynom
`0xA001`, reflekterad, init `0000`, XorOut `0000`, verifierad mot det kända
testvärdet `"123456789"` → `BB3D`), beräknad över filens UTF-8-bytes
(utan BOM). Checksumman läggs till i filnamnet som fyra versala hexsiffror:
`{filnamn}_{CRC}.xml`, t.ex. `travreda-V85-2026-08-25_A1B2.xml` — inte i
själva XML-innehållet. `index.html` gör nu detta automatiskt
(`crc16HexFromString()`), verifierat genom att oberoende räkna om
checksumman för en riktig nedladdad fil i Node.js och jämföra mot
filnamnet.

**Fortfarande inte bekräftat:** om felmeddelandet försvinner helt med
checksumman på plats, eller om filen faktiskt går igenom till spel utan
fler varningar — nästa verkliga inlämningsförsök avgör det.

### Automatisk inlämning till ATG — undersökt, inte möjlig

Användaren frågade om Travreda kunde skicka in systemet direkt till ATG,
som Jokersystemet och andra verktyg verkar göra. Undersökt genom att läsa
[HPTClients](https://github.com/Hospodaren/HPTClient) källkod direkt
(`UCMarksGame.xaml.cs`, `miSaveAndGoToATG_Click`) och research kring ATG:s
API-utbud. Slutsats: **det finns ingen genväg** — inte ens i HPTClient.

- HPTClients "spara och gå till ATG"-knapp gör bara `Clipboard.SetDataObject
  (filnamn)` + `wbATG.Navigate("https://www.atg.se/spel/fil")` i en inbyggd
  webbläsarruta — samma manuella filuppladdning som Travreda redan har, bara
  med urklipp-ifyllnad och utan att byta fönster. Ingen riktig API-inlämning.
- ATG har en riktig programmatisk vadslagnings-API (**ABI, "ATG Betting
  Interface"**, hittad via `swedishhorseracing.com/for-partners`) — men den
  är en företagsintegration för **certifierade internationella
  spelbolag/totalisatorer**, inte något en privatperson kan skaffa nyckel
  till.
- Även om åtkomst funnits hade det inte gått att bygga in i en statisk
  webbsida ändå: ingen inramning av atg.se är möjlig (troligen
  `X-Frame-Options`/CSP mot clickjacking, standard för spelsajter), och en
  webbsida kan inte lägga en nedladdad fils sökväg på operativsystemets
  urklipp åt en filväljardialog på en annan sajt (skulle vara ett
  säkerhetshål om det gick).

**Byggt istället:** `#btn-open-atg` ("Öppna ATG:s filinlämning") direkt
efter nedladdningsknappen, öppnar `atg.se/spel/reducerat` i en ny flik
(`window.open(..., "_blank", "noopener")`) — samma URL som redan låg i
förklaringstexten som en vanlig länk, nu som en tydlig egen knapp i
handlingsflödet ladda ner → öppna ATG. Detta är själva taket för vad en
statisk sida kan göra här; motsvarar exakt HPTClients bekvämlighet minus
urklipps-tricket, som webbläsare av säkerhetsskäl inte tillåter.

### Kupongkomprimering (exakt, tre nivåer)

Byggt efter uttrycklig begäran om att hålla ner antalet kuponger (mål:
under 100 för ett typiskt system på 30 000–40 000 rader) **utan att någonsin
täcka en enda rad som inte uppfyller villkoren** — användaren svarade
uttryckligen nej på frågan om överdäckning (extra, icke-villkorsuppfyllande
kombinationer) var acceptabelt, så alla tre nivåer är 100 % exakta.

**Varför det är svårt:** en ATG-kupong kan bara uttrycka "vilken som helst
av dessa hästar" *inom en enda avdelning* (`marks`-bitmasken är oberoende
per `<leg>`). Den kan inte uttrycka ett villkor som gäller summan av en
bokstav över flera avdelningar. Rader kan därför bara slås ihop till en och
samma kupong om de delar **exakt samma bokstavsmönster** (vilken bokstav
varje avdelning bidrar med) — annars skulle kupongen även täcka
kombinationer som villkoren inte tillåter.

- **Okomprimerad** (`compressionLevel = "none"`) — en kupong per rad, som
  ursprungliga v1.
- **Lättare komprimering** (`"light"`, **standard**) — `buildPatternBoxes()`
  grupperar raderna efter bokstavsmönster via en backtracking-sökning
  (`dfs()` i funktionen, med tidig avbrytning så fort ett villkors min/max
  omöjligt kan uppfyllas med kvarvarande avdelningar). Bokstäver som inte
  förekommer i något villkor (t.ex. B/D när villkoren bara gäller A/C)
  slås ihop till en gemensam `"OTHER"`-grupp per avdelning eftersom de inte
  påverkar om villkoren uppfylls — det är den här sammanslagningen som gör
  att redan denna nivå ofta ger en stor kompression (antalet *mönster* är
  ofta mycket mindre än antalet rader, särskilt när flera hästar delar
  bokstav i en avdelning). Helt exakt: varje rad hör till exakt ett mönster
  (dess egna bokstäver per avdelning), så mönster-kupongerna är en ren
  partition av radmängden, aldrig en approximation.
- **Hårdare komprimering** (`"hard"`) — efter Lättare, `compressHard()`
  kör `mergeBoxesOnce()` upprepade gånger: hitta grupper av mönster-kuponger
  som är identiska i **alla avdelningar utom en**, och slå ihop dem genom
  att unionera hästarna i just den avdelningen. Matematiskt säkert (om två
  mönster var för sig redan uppfyller villkoren oavsett den ena
  avdelningens bokstav, gör vilken kombination som helst av de
  sammanslagna hästarna det också) — analogt med hur Quine-McCluskey slår
  ihop angränsande minterm i logikminimering, fast med bokstäver istället
  för bitar och upp till 8 dimensioner. Körs till en fixpunkt (inga fler
  sammanslagningar möjliga), begränsat av en säkerhetsspärr på
  `legCount × 5` iterationer (rent defensivt — varje lyckad
  sammanslagningsrunda minskar kupongantalet strikt, så en oändlig loop är
  inte möjlig i praktiken).

**Verifierat exakt** dels med en fristående Node-testfil (syntetiska
8-avdelningssystem, jämför den fulla raduppsättningen från `generateRows()`
mot samma uppsättning uppackad ur kupongerna — alla scenarier gav 100 %
matchning, inklusive ett 41 118-raders system nära användarens angivna
typiska storlek som gick från 458 kuponger (Lättare) till 80 (Hårdare)),
dels end-to-end i en riktig webbläsare (Playwright, riktig V85-fixture):
23 920 rader → 1 207 kuponger (Lättare) → 168 kuponger (Hårdare), export-
XML:en parsad och uppackad tillbaka till radnivå för alla tre nivåer,
exakt likadan raduppsättning i samtliga fall.

**Priset påverkas inte** — komprimering ändrar bara hur få fysiska
kupongrader som behövs i exportfilen, inte hur många kombinationer som
faktiskt spelas. `liveStats.rows`/priset räknas alltid från de faktiska
raderna (`generateRows()`), oberoende av vald komprimeringsnivå.
`liveStats.coupons` är det separata talet som visas i sammanfattningen och
avgör hur många `<coupon>`-element exportfilen får.

**Inget nytt prestandaproblem:** mönster-sökningen jobbar med det
*reducerade alfabetet* (antal villkorsstyrda bokstäver + 1 för "OTHER" per
avdelning, i praktiken högst 3 med de fördefinierade presets: A, C, OTHER)
upphöjt till antal avdelningar — några tusen noder i värsta fall, oberoende
av hur många hästar per bokstav. Ingen koppling till `LIVE_STATS_MAX`
(200 000, som bara gäller den råa radgenereringen).

**Inställning:** en radioknappsgrupp (`compression-level`) under
Inställningar, samma mönster som sorteringsvalet, sparad i egen
localStorage-nyckel (`travreda-compression`, global inställning precis som
`travreda-sort-order` — inte kopplad till en specifik omgång). Byte av nivå
kör om `refreshLiveStatsAndUI()` direkt så sammanfattningen och sticky-
knappen uppdateras utan att behöva trycka på "Beräkna rader".

---

## 7. Reduceringslogik — ABC(D)-bokstavshinkar + villkor

Medvetet vald **klassisk bokstavsmodell**, inte Jokersystemets poängsystem
(som använder ett numeriskt poäng per häst + en poängsummegräns över hela
systemet — se konversationshistorik för ett verkligt exempel). Användaren
valde uttryckligen bokstäver istället, trots att det egna Jokersystemet-
exemplet faktiskt visade poängmodellen.

- Varje häst i varje avdelning får **Ej vald / A / B / C / D**, antingen
  via en `<select>` eller via stegvisa knappar (se "Bokstavsval:
  knappar eller meny" nedan). "Ej vald" = hästen är inte en kandidat alls
  i systemet.
- **Villkor** (valfria, adderande, en per bokstav): "Bokstav X: minst N,
  högst M" räknat över **hela systemet** (alla avdelningar tillsammans) —
  t.ex. minst 2 A-hästar rätt. Utan villkor blir systemet hela
  korsprodukten av de bokstavsmärkta hästarna (enklaste ABC-fallet).
- **Oreducerat/Reducerat-antal** visas löpande (se "Live sammanfattning och
  insatsprocent per häst" nedan), med en varning och bekräftelse-knapp om
  den oreducerade korsprodukten är väldigt stor (>3 miljoner kombinationer,
  `MAX_UNREDUCED_WARN`) innan en tvingad beräkning faktiskt körs — annars
  kan webbläsaren hänga sig.

### Bokstavsval: knappar eller meny

**Bakgrund:** användaren upplevde `<select>`-menyns fokus-/svephantering
som krånglig med VoiceOver ("lite trassel med fokus och när man sveper
runt"). En ny inställning under Inställningar, **"Bokstavsval"**
(`letterInputMode`, `"buttons"` | `"menu"`, sparas i
`travreda-letter-input-mode`), låter användaren välja mellan de två —
**knappar är standard**.

- **Knappläget** ersätter menyn med 1–2 knappar som stegar igenom kedjan
  `Ej vald ↔ A ↔ B ↔ C ↔ D` (`LETTER_SEQUENCE`). Vid ändpunkterna
  (Ej vald, D) visas bara en knapp — antalet knappar växlar alltså mellan
  1 och 2, på uttrycklig begäran (inte en alltid-synlig men inaktiverad
  knapp, till skillnad från t.ex. Flytta upp/ner-knapparna för
  detaljradernas ordning). Knapparnas synliga text **är** destinationen
  (t.ex. "B" eller "Ej vald") — ingen separat värdetext behövs eftersom
  statusetiketten på hästkortet (`updateSelectionLabel()`, "Vald B 65%,")
  redan visar aktuellt läge. `aria-label` är kort och konsekvent för byte
  mellan redan valda bokstäver ("Byt till B" / "Ta bort bokstav") — hästens
  namn behöver inte upprepas där eftersom VoiceOver redan läst upp det via
  hästkortets egen knapp precis innan. **Undantag, på uttrycklig begäran:**
  knappen som väljer hästen första gången (från "Ej vald", alltid till "A")
  heter istället `"Välj {nummer} {namn}"` — den handlingen är den egentliga
  urvalshandlingen (bokstaven är ändå alltid "A" härifrån), så numret/namnet
  är mer relevant att läsa upp än bokstaven.
- **Egen bakgrundsfärg** (`--stepper-bg`, en mörkorange ton skild från både
  den ljusare CTA-orangen och den marinblå standardknappsfärgen) på
  uttrycklig begäran, så knapparna syns tydligare bredvid hästkortets egen
  (marinblå) knapp.
- **Menyläget** är den ursprungliga `<select>`:n, oförändrad.
- Struken häst visar **inga** knappar alls i knappläget (samma "hellre
  tyst"-princip som resten av appen) — motsvarar den inaktiverade,
  fortfarande synliga `<select>`:n i menyläget, bara utan en overksam
  kvarliggande kontroll.
- Bytet mellan lägena är rent visuellt — påverkar inte `legLetters`-datan,
  villkorslogiken eller exporten. Verifierat med Playwright: bokstaven som
  redan var vald i knappläget (t.ex. D) fanns kvar oförändrad efter byte
  till menyläget, och tvärtom.

### Fördefinierade villkor

En rullista (`#villkor-preset`) i Villkor-vyn med sex färdiga
bokstavsvillkor plus ett specialläge, i denna ordning:

1. Minst 2 A-hästar och max 1 C-häst (**förvalt** — `DEFAULT_PRESET_ID`,
   sätts automatiskt när en ny omgång laddas första gången)
2. **Vanligt matematiskt system utan reducering** (`systemMode = "plain"`)
   — flyttad hit från sista platsen på användarens begäran, för synlighet
   direkt efter förvalet
3. Minst 1 A-häst
4. Minst 2 A-hästar
5. Minst 1 A-häst och max 1 C-häst
6. Minst 3 A-hästar och max 1 C-häst
7. Minst 3 A-hästar och max 2 C-hästar

Introtexten i Villkor-vyn nämner numera uttryckligen att "Vanligt
matematiskt system utan reducering" finns som ett eget alternativ i
listan, så det inte bara upptäcks av en slump.

Att välja ett villkor i listan skriver **över** hela `villkor`-arrayen med
det förvalda villkoret — det är en snabb tillämpning, inte en sparad koppling
till den exakta rullistevalen (manuell redigering av villkor efteråt
återspeglas inte tillbaka i rullistan, förutom för specialläget "Vanligt
system", se nedan).

**Ingen manuell villkor-redigering längre** — det tidigare gränssnittet med
en rad per villkor (bokstavsväljare + min/högst-fält + ta bort-knapp) är
helt borttaget på användarens begäran ("dom behövs inte längre"). Rullistan
med fördefinierade villkor är nu det enda sättet att sätta/ändra villkor —
`villkor`-arrayen finns fortfarande internt (`presetToVillkor()` bygger
den), men det finns inget UI för att se eller finjustera den rad för rad.
Istället visas en enkel, skrivskyddad sammanfattning: **`#letter-tally`**
(`renderLetterTally()`) räknar hur många hästar som är märkta med
respektive bokstav över hela systemet (alla avdelningar), t.ex.
"8 A-hästar, 0 B-hästar, 0 C-hästar, 0 D-hästar." — räknar bara markerade
hästar, oberoende av om något villkor faktiskt är aktivt. Ligger **direkt
under** `<h2>Systemöversikt</h2>` (flyttad dit från platsen direkt under
rullistan, på uttrycklig begäran) och är **duplicerad** på samma sätt som
resten av Systemöversikt (se nedan) — `#avd-letter-tally` visar samma text
direkt under motsvarande rubrik i avdelningsvyn. `renderLetterTally()`
skriver till båda elementen i samma anrop, och anropas nu även från
`refreshLiveStatsAndUI()` (inte bara `renderVillkor()`) så att
avdelningsvyns kopia uppdateras live vid varje ändring, inte bara när man
navigerar till Villkor-vyn.

**Motsvarande bokstavsuppdelning per avdelning** (`buildMarkedCountText()`,
delad mellan den initiala renderingen och `markChanged()` för att inte
duplicera logiken) läggs till på `#avd-marked-count` i huvudvyn, t.ex.
"5 av 12 hästar markerade i den här avdelningen, 1 a-häst, 2 b-hästar,
2 c-hästar." Medvetet annorlunda från `#letter-tally` ovan på två sätt,
efter användarens egna exempel: gemener (`a-häst` inte `A-häst`) och
**bokstäver med noll hästar utelämnas helt** (visar inte "0 d-hästar") —
den globala sammanställningen visar även nollor, men den här kortare
per-avdelningsraden ska bara nämna bokstäver som faktiskt används där.

`systemMode` (`"abc"` | `"plain"`, sparas per omgång i `saveState()`) styr
vilken kontroll som visas per häst i avdelningsvyn:

- `"abc"` (normalläge): `<select>` eller stegvisa knappar, se ovan.
- `"plain"`: internt sätts bokstaven `"A"` när hästen är vald, precis som om
  hästen manuellt valts som A i vanligt läge. Eftersom villkor samtidigt
  töms (`rules: []`) blir resultatet hela korsprodukten av valda hästar,
  utan reducering — ingen ändring behövdes i
  `buildCandidates()`/`generateRows()`/export, de bryr sig bara om att en
  bokstav finns satt, inte vilken.
  **Var ursprungligen en `<input type="checkbox">` + `<label>`, nu en enda
  togg-knapp** (`aria-pressed`, samma mönster som bokstavsstegraren ovan) —
  ändrat efter en rapporterad VoiceOver-upplevelse av två svep per häst
  (hästkortets egen knapp, sedan kryssrutan). Ett riktigt "ett enda svep"
  hade krävt att slå ihop namn-knappen och valkontrollen till samma
  element, vilket hade tagit bort den separata "visa detaljer"-funktionen
  — den här lösningen gör istället kontrollen konsekvent med ABC-lägets
  knappar och undviker kryssrutans ibland mer utförliga uppläsning. Samma
  text som förut: `"Vald"` intryckt, `"Ej vald"` ej intryckt — `aria-label`
  stavar ut handlingen med nummer och namn (`"Välj 6 Princess Diamond"` /
  `"Ta bort 6 Princess Diamond"`).
- Byter man till ett riktigt villkor (rullistan eller "Lägg till eget
  villkor") växlar `systemMode` automatiskt tillbaka till `"abc"` och
  hästlistan ritas om med bokstavsväljare — redan ikryssade hästar (bokstav
  "A") följer med rätt över.

### Live sammanfattning och insatsprocent per häst

Byggt efter uttrycklig begäran: *"Det är viktigt att förstå hur mycket av
insatsen som läggs på respektive vald häst när villkoren är aktiva"* — och
att detta ska uppdateras **automatiskt**, inte bara vid tryck på en
"Beräkna"-knapp.

**`computeLiveStats(forceHuge)`** är den enda platsen som faktiskt genererar
rader (`generateRows()`) och sätter det globala `liveStats`-objektet
(`{tooBig, unreduced, rows, perLegCounts}` — `perLegCounts` är en array,
en post per avdelning, med `{startnummer: antal godkända rader som
innehåller den hästen}`). Körs automatiskt (`forceHuge=false`) efter
**varje** ändring (bokstavsval, kryssruta, villkor-preset) via
`refreshLiveStatsAndUI()`, anropad från `markChanged()` och i slutet av
`renderAvdelning()`.

- **Prestandaspärr (`LIVE_STATS_MAX`, 200 000):** är den oreducerade
  korsprodukten större än så, körs **ingen** automatisk beräkning — bara
  ett `{tooBig:true}`-läge sparas, och texten ber användaren trycka på
  "Beräkna rader" manuellt istället. Detta är en lägre, "tyst" spärr än den
  gamla `MAX_UNREDUCED_WARN` (3 miljoner) som fortfarande gäller för den
  manuella knappen (`btn-calculate`, `computeLiveStats(true)`) — där visas
  istället en `confirm()`-dialog eftersom ett explicit knapptryck är en
  medveten handling, till skillnad från en automatisk bakgrundsberäkning
  efter varje litet bokstavsval.
- **Insatsprocent per häst** (i `updateSelectionLabel()`, samma funktion
  som redan byggde "Vald A-häst"-etiketten): är `liveStats` färskt och
  `rows > 0`, räknas `perLegCounts[avdelning][startnummer] / liveStats.rows
  × 100` och läggs till direkt efter statusetiketten. Saknas `liveStats`
  (inga hästar markerade i alla avdelningar än, eller `tooBig`), visas ingen
  procent alls.
  **Förkortad på uttrycklig begäran** (var `"Vald A-häst, 65% av
  insatsen. 1 Varenne, ..."` — bokstaven fick eget "-häst"-suffix, ett eget
  kommatecken, och "% av insatsen" utskrivet, sedan en punkt som bröt av
  innan hästnamnet): är nu `"Vald A 65%, 1 Varenne, ..."` — inget
  "-häst"-suffix, procenten skrivs direkt efter bokstaven utan mellanliggande
  komma, och hela etiketten avslutas med **komma** (inte punkt) så den
  flyter ihop med resten av den redan kommaseparerade huvudraden istället
  för att bryta av som en egen mening. Gäller även Vanligt matematiskt
  system (`"Vald 65%, ..."`, inget bokstavsled).
- **Registrering av uppdaterare:** varje hästrad registrerar sin egen
  `updateSelectionLabel` i den modulglobala `currentRowUpdaters`-arrayen
  (nollställd i början av varje `renderAvdelning()`). `refreshLiveStatsAndUI()`
  kör om **alla** registrerade uppdaterare efter varje omräkning — så även
  hästar i **andra** avdelningar (inte bara den man just ändrade i) får sin
  insatsprocent uppdaterad, eftersom en ändring i avdelning 3 påverkar hur
  insatsen fördelas i alla åtta avdelningar. Uppdaterar bara textinnehåll,
  bygger inte om DOM-element — samma "uppdatera bara det som ändrats"-
  princip som VO Turf List använder för att inte störa en pågående
  VoiceOver-svepning.

**Sticky knapp (`#btn-sticky-summary`)** längst ner i avdelningsvyn (Jokersystemet-
inspirerad, byggd efter uttrycklig begäran) visar och läser upp
(`aria-live="polite"` direkt på knappen) samma sammanfattning i kompakt
form: `"{oreducerat} rader, reducerat {X} %, {reducerat} rader, pris {kr}
kr, {N} kuponger."` — `{X}` är hur många procent som **togs bort** av
villkoren (`100 − (reducerat/oreducerat×100)`), inte hur många som blev
kvar. Kupongantalet utelämnas bara vid `compressionLevel === "none"`
(redundant mot radantalet där). Ett tryck navigerar till Villkor-vyn
(`showView("villkor")`) där **exakt samma text** (`coreText` i
`renderLiveSummary()`) visas i `#summary-text`, fetstilad, med en extra
rad om prisantagandet under — de två visar alltså aldrig olika/inaktuella
tal, på uttrycklig begäran ("sammanfattningen ... presenteras likadant som
på knappen"). **Dold helt** (`#sticky-footer[hidden]`, inte en vägledande
text som tidigare) tills alla åtta avdelningar har minst en markerad häst
— `liveStats` är `null` exakt i det läget (`computeLiveStats()` sätter
aldrig `liveStats` om någon avdelnings kandidatlista är tom), så
`renderLiveSummary()` togglar `stickyFooter.hidden` på samma villkor som
den redan använde för att avgöra "inget att visa än". Ändrat på uttrycklig
begäran — knappen hade inget meningsfullt att visa innan dess, samma
"hellre tyst"-princip som resten av appen.

**Visuell prominens (byggd efter uttrycklig begäran — knappen "syntes inte"):**
`class="btn-primary"` (samma gula accentfärg som andra viktiga knappar,
t.ex. "Beräkna rader") istället för den vanliga grå standardknappsstilen,
plus egen, något större `font-size`/`padding` (`#btn-sticky-summary` i
CSS). `.sticky-footer` fick också extra `padding-bottom` via
`env(safe-area-inset-bottom, 0px)` (samma mönster som VO Turf List
använder för sina sticky-knappar) så att knappen inte sitter klistrad i
absolut skärmkant utan har lite luft nedåt.

**Smalare och mer luft ovanför (byggd efter uttrycklig begäran):**
`.sticky-footer button`s `max-width` minskad från `28rem` till `16rem` —
knappen är fortfarande centrerad (`.sticky-footer{justify-content:center}`),
bara smalare än tidigare fullbreddsknappen. `.sticky-footer`s toppmargin
ökad från `1rem` till `3.5rem` så det blir tydligt mer avstånd mellan
hästlistan/systemöversikten ovanför och knappen — den är fortfarande
`position:sticky;bottom:0` (glider fast i skärmens nederkant när man
scrollat förbi den), bara med mer luft innan den träder in.

`renderLiveSummary()` är den enda platsen som skriver till
`#btn-sticky-summary`, `#summary-text`, `#calc-status` och togglar
`#btn-export`s `disabled`-status — både den automatiska vägen
(`refreshLiveStatsAndUI`) och den manuella knappen (`btn-calculate`) går
via samma funktion, så de två aldrig kan visa olika/inaktuella tal.

### Systemöversikt

Egen `<h2>` i Villkor-vyn, direkt efter bokstavssammanställningen
(`#letter-tally`), byggd efter uttrycklig begäran om att se exakt vilka
hästar som är markerade i varje avdelning utan att behöva bläddra dit.
`renderSystemOverview()` anropas både från `renderVillkor()` (vid
navigering till vyn) och `refreshLiveStatsAndUI()` (vid varje ändring i
avdelningsvyn), samma dubbla anropsmönster som `renderLiveSummary()`.

- **`#system-overview-unreduced`** ("Oreducerat: X kombinationer.") visas
  bara när `liveStats` är färskt (alla avdelningar har minst en markerad
  häst) — annars döljs den helt, samma "hellre tyst"-princip.
- Per avdelning byggs en `<h3>` ("Avd N: X hästar valda:") följt av, i
  ABC-läge, en `<p>` per bokstav som faktiskt har markerade hästar
  (`"A: 5, 9."`) — bokstäver utan träffar utelämnas helt, samma princip
  som `#avd-marked-count`s bokstavsuppdelning. En avdelning utan några
  markerade hästar visar ändå sin `<h3>` ("0 hästar valda:") men inga
  bokstavsrader — **varje** avdelning listas alltid, till skillnad från
  andra "hellre tyst"-ställen i appen, eftersom hela poängen är en
  fullständig översikt.
- **Vanligt matematiskt system:** hela avdelningen radas upp på samma rad
  som rubriken istället ("Avd 1: 4 hästar valda: 6, 7, 9, 10.") — ingen
  bokstavsuppdelning behövs eftersom alla ikryssade hästar internt är
  bokstaven "A", på uttrycklig begäran ("kan varje avdelning presenteras
  på samma rad").

**Duplicerad längst ner i avdelningsvyn** (`#avd-system-overview`/
`#avd-system-overview-unreduced`, egen `<h2>`), på uttrycklig begäran om
att alltid kunna följa vilka hästar man valt utan att navigera bort från
startlistan. Samma innehåll visas på **båda** ställena (bekräftat: inte
en flytt, en riktig duplicering) — `renderSystemOverview()` byggdes om
till en tunn wrapper som anropar en delad `buildSystemOverviewInto(container,
unreducedEl)` två gånger, en gång per plats, så de aldrig kan divergera.
Placerad direkt under `#horse-list`, före `#autosave-status`. Verifierat
med Playwright att båda ställena renderar exakt identisk HTML vid varje
ändring.

---

## 8. Arkitektur

### Vyer

`view-start` (välj omgång, automatiskt från `data/games.json` eller manuellt
datum+bankod), `view-avdelning` (huvudsidan: sticky avdelningsflikar + meny,
en avdelning i taget: häst/kusk/tränare/procent/barfota + bokstavsval eller
kryssruta), `view-villkor` (villkor, sammanfattning, export),
`view-installningar` (sorteringsval, mer kommer). Enkel vy-växling, ingen
History API ännu (kan läggas till senare om det behövs).

### Tips och instruktioner (Startsidan)

Expanderbar knapp (`#btn-tips-toggle`, `aria-expanded`/`aria-controls`,
samma öppna/stäng-mönster som meny-knappen i avdelningsvyn och hästkortens
detaljvy) direkt efter beskrivningen på Startsidan, före "Kommande
omgångar" — samma placering och idé som VO Turf Lists "Tips &
instruktioner", men medvetet mycket kortare (två korta stycken, inte VO
Turfs ~18 punkter över åtta rubriker) eftersom Travredas flöde är
betydligt enklare. Innehåller en kort "Så fungerar det"-sammanfattning av
hela flödet (välj omgång → bokstavsmarkera → villkor → beräkna → exportera)
och en punktlista över de tre inställningarna som finns. En egen
"Stäng instruktioner"-knapp längst ner i panelen, samma mönster som
`btn-minimize` på hästkorten.

### Datamodell

```js
currentGame = { type, id, date, trackId, trackName, races: [...] }
letters = { [avdelningsindex]: { [startnummer]: 'A'|'B'|'C'|'D' } }
villkor = [{ letter, min, max }, ...]
systemMode = 'abc' | 'plain'
sortOrder = 'procent' | 'startnummer'
```

### Inställningar — sortering av startlistor

Två radioknappar (`sort-procent`/`sort-startnummer`, `name="sort-order"`)
under Inställningar. **Spelprocent (mest spelade häst överst)** är standard
— sorterar fallande på `pools[type].betDistribution`, samma fält som redan
visas på huvudraden. **Startnummer** sorterar stigande på `start.number`
(ATG:s egen, "naturliga" ordning). Sparas i en egen localStorage-nyckel
(`travreda-sort-order`, separat från `travreda-state-v1` eftersom det är en
global appinställning, inte kopplad till en specifik omgång) och gäller
direkt vid byte, oavsett vilken omgång som är laddad.

### localStorage — automatisk sparning

**Bakgrund:** rapporterad bugg — användaren tappade allt ifyllt (bokstäver,
villkor, vald avdelning) vid flikbyte i mobil webbläsare. Orsak: mobil
Safari kan tömma en bakgrundsflikens minne helt för att spara RAM/batteri;
växlar man tillbaka laddas sidan om från noll, och all appstate låg bara i
JS-variabler utan något att återställa från.

**`travreda-state-v1`** — en enda JSON-blob: `{game, letters, villkor,
currentAvd, savedAt}` där `game` är precis det som behövs för att hämta om
omgången (`type/id/date/trackId/trackName`) — själva startlistan/oddsen
hämtas alltid färskt igen från ATG vid återställning, bara dina val
(bokstäver/villkor/avdelning) sparas och läses tillbaka.

**`saveState()`** anropas efter **varje** förändring (bokstavsval, lägg
till/ändra/ta bort villkor, byte av avdelningsflik) — inte bara vid någon
explicit "spara"-knapp, så även ett abrupt avbrutet tabbyte tappar minimalt.
Extra skyddsnät utöver det: `visibilitychange` (fliken döljs) och
`pagehide` utlöser också ett sparförsök, ifall något enstaka
mutationsställe skulle missas. `localStorage`-anrop är inbäddade i
`try/catch` — privat surfläge eller fullt lagringsutrymme får appen att
fortsätta fungera utan att spara, istället för att krascha.

**Vid sidladdning** läses `travreda-state-v1` in före `loadGamesList()`
hinner rendera Startsidan — finns sparad data hämtas omgången om via
samma `loadGame()`, men med bokstäver/villkor/avdelning återställda istället
för nollställda, och användaren hamnar direkt på huvudsidan igen istället
för Startsidan. Misslyckas återhämtningen (omgången kan ha avslutats)
visas ett tydligt felmeddelande och den sparade datan lämnas orörd.

En liten textrad (`#autosave-status`, "Sparat automatiskt kl HH:MM.") på
huvudsidan bekräftar synligt att sparningen faktiskt sker, i samma stil som
`#status-msg`/`#nav-status` i VO Turf List — ingen `aria-live`, bara vanlig
uppdaterad text. Placerad direkt under startlistan (`#horse-list`), inte
högst upp bland de andra statusraderna — flyttad dit på användarens
begäran för att inte ta plats/uppmärksamhet högst upp på sidan.

**Ej byggt:** inloggning eller serverlagring — bedömdes som en stor
överdrift (kräver backend/databas/autentisering) för ett personligt
verktyg med en användare, och bryter mot enfils/ingen-server-principen.
`localStorage` löser det faktiska problemet (data överlever flikbyte och
hel omladdning) utan den komplexiteten.

### Skydd mot att tappa ett system av misstag

**Bakgrund:** användaren frågade vad som händer om man vill bygga ett nytt
system för samma omgång (t.ex. går tillbaka till Startsidan och väljer
samma omgång igen) — `loadGame()` utan `restoreData` nollställer tyst
`letters`/`villkor`/`systemMode`, och `saveState()` skriver omedelbart över
den sparade datan, så det fanns ingen väg tillbaka.

- **`hasAnyMarkedLetters()`** — sant om minst en häst i någon avdelning har
  en bokstav satt.
- **`confirmDiscardIfNeeded()`** — visar en `confirm()`-dialog ("Du har
  redan markerat hästar i ett pågående system. Fortsätta och rensa det?")
  bara om `hasAnyMarkedLetters()` är sant. Anropas av **båda** ställena som
  kan starta en ny omgångsladdning: knapparna i omgångslistan på Startsidan
  och den manuella datum/bankod-inmatningen (`btn-manual-load`) — precis
  före respektive `loadGame()`-anrop, aldrig inuti `loadGame()` självt, så
  den vanliga automatiska återställningen vid sidladdning (som skickar
  `restoreData`) aldrig påverkas. Avbryter man dialogen (`confirm()`
  returnerar `false`) händer ingenting — ingen laddning sker, systemet
  ligger kvar orört.
- **`clearSystem()`** — ny knapp **`#btn-clear-system`** ("Rensa system") i
  Villkor-vyn, direkt efter villkor-rullistan. Egen `confirm()`-dialog
  ("Rensa alla bokstavsmarkeringar i det här systemet?"), och nollställer
  vid bekräftelse `letters`, `systemMode` (tillbaka till `"abc"`) och
  `villkor` (tillbaka till förvalet `DEFAULT_PRESET_ID`, samma
  `presetToVillkor()`-anrop som `loadGame()`s eget resetblock använder) utan
  att lämna omgången — till skillnad från att ladda om omgången helt,
  behåller detta startlistan/oddsen som redan är hämtade. Ritar om
  Villkor-vyn (`renderVillkor()`) och sparar (`saveState()`) direkt.

Verifierat med Playwright mot en riktig V85-fixture: bekräftad omladdning
av samma omgång med markeringar utlöser exakt en dialog och nollställer
`#avd-marked-count` till `"0 av N hästar markerade."`; en omladdning med
**tomt** system (inga markeringar) utlöser **ingen** dialog alls; "Rensa
system" utlöser sin egen dialog och nollställer på samma sätt utan att
lämna Villkor-vyn.

---

## 9. Kända begränsningar i v1

- Bara V85, V75, V86 (samma XML-struktur, olika antal avdelningar/tagg).
- Ingen reservhästhantering i exporten.
- Ingen kupong-komprimering — kan ge stora filer vid breda system.
- Radpris per speltyp (se `ROW_PRICE` i avsnitt 6) vilar för fem av sex
  typer bara på ATG:s kundtjänstguide, inte ett eget verkligt inlämnat
  exempel (bara V85 är bekräftat så, via Jokersystemet-PDF:en).
- Spel-id-upptäckt (GitHub Action) ej körd/verifierad över flera dagar än —
  bör observeras några dagar för att bekräfta att den håller sig uppdaterad.
- **Tre verkliga inlämningsförsök (V86) avvisades** ("Angivet spel är inte
  tillgängligt") innan grundorsaken hittades, se avsnitt 5: två gällde fel
  bankod (första gången `tracks[0]`-gissningen, andra gången det då
  antagna men fortfarande felaktiga "avdelning 1:s fysiska bana") och ett
  gällde en omgång som redan hunnit starta (statusen hade gått från
  `bettable` till `ongoing`, en proaktiv varning + export-spärr för detta
  finns sedan tidigare, se avsnitt 5). Bankoden hämtas nu ur spel-id:ts
  egen inbäddade bankodskomponent — verifierad mot tre oberoende källor
  och med Playwright, se avsnitt 5 — men ett nytt, lyckat, verkligt
  inlämningsförsök efter denna sista fix är **inte bekräftat än**.
- Ingen engelsk översättning (bara svenska, till skillnad från VO Turf List).

---

## 10. Snabbreferens vid start av ny konversation

1. Läs denna fil
2. Läs `index.html` för att förstå nuläget
3. Fråga vad användaren vill åstadkomma
4. **Diskutera (en fråga i taget) → bekräfta → bygg → verifiera → uppdatera
   tidsstämpel → presentera**
