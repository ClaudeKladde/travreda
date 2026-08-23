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
<span class="update-line">Vibe coded with Claude, senast uppdaterad ÅÅÅÅ-MM-DD HH:MM</span>
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
- **Tystnad hellre än brus:** nämn bara barfota när hästen faktiskt går
  barfota (inte "skor på" för varje häst) — samma "hellre tyst än onödigt
  pratig"-princip som VO Turf List.
- **Fokushantering:** flytta fokus till avdelningens rubrik
  (`tabindex="-1"`) när man byter avdelning, så VoiceOver-användare inte
  tappar sammanhanget.
- **Standardkontroller:** `<select>` för bokstavsval (Ej vald/A/B/C/D) i
  normalläge, `<input type="checkbox">` i "Vanligt system"-läget, istället
  för egenbyggda widgets — robust med VoiceOver utan extra ARIA.
- **Mörkt läge som standard**, tydliga kontraster, gul färg (`--accent`) för
  visuellt markerade/valda hästar.
- Inga emoji i gränssnittet.

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
  `sulkyMainRowText()`/`shoesInfo()` returnerar numera texten utan eget
  avslutande skiljetecken (huvudradens `subParts`-array lägger till rätt
  tecken beroende på position).
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

Menyknappen (`.menu-wrap`) är `position:absolute` i sticky-radens
övre högra hörn, medvetet borttagen ur flikradens flex-flöde (`.avd-tabs`
har `padding-right` som reserverar plats åt den) — annars konkurrerar
menyknappens bredd med flikarna om utrymmet och tvingar den sista fliken
att radbryta för sig själv. Flikstorleken (`.avd-tab`, ~1,9 rem) är avpassad
för att rymma alla 8 avdelningar på en rad även på en smal mobilskärm.

**Tabbordning:** `.menu-wrap` ligger nu **före** `.avd-tabs` i DOM:en (på
användarens begäran, för att nå menyn utan att först behöva svepa/tabba
förbi alla avdelningsknapparna) — påverkar bara läsordning/tabbordning,
inte det visuella utseendet, eftersom `.menu-wrap` redan var absolut
positionerad och alltså opåverkad av var den ligger i flödet.

**Sidhuvudets ordning på huvudsidan** (`view-avdelning`): `#avd-progress`
(omgångens namn: "V85 — Romme — 2026-08-22") och `#avd-turnover`
(omsättning) ligger nu **högst upp på sidan**, före den sticky menyraden
— på användarens begäran, så att omgångens sammanhang läses innan man når
avdelningsflikarna/menyn. Ordningen är: `avd-progress` → `avd-turnover` →
`.topbar` (meny + flikar) → `avd-heading` (lopprubrik) → `avd-terms` (se
nedan) → `avd-marked-count` → hästlistan.

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

**Radpris:** antaget 0,50 kr/rad (bekräftat via Jokersystemet-exemplet:
1865 rader × 0,50 kr = exakt 932,50 kr som visades i deras PDF) — **inte
bekräftat direkt mot ATG för V85 specifikt**, dubbelkolla alltid faktiskt
pris på atg.se innan du lämnar in en fil.

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

- Varje häst i varje avdelning får **Ej vald / A / B / C / D** via ett
  `<select>`. "Ej vald" = hästen är inte en kandidat alls i systemet.
- **Villkor** (valfria, adderande, en per bokstav): "Bokstav X: minst N,
  högst M" räknat över **hela systemet** (alla avdelningar tillsammans) —
  t.ex. minst 2 A-hästar rätt. Utan villkor blir systemet hela
  korsprodukten av de bokstavsmärkta hästarna (enklaste ABC-fallet).
- **Oreducerat/Reducerat-antal** visas löpande (se "Live sammanfattning och
  insatsprocent per häst" nedan), med en varning och bekräftelse-knapp om
  den oreducerade korsprodukten är väldigt stor (>3 miljoner kombinationer,
  `MAX_UNREDUCED_WARN`) innan en tvingad beräkning faktiskt körs — annars
  kan webbläsaren hänga sig.

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
Istället visas en enkel, skrivskyddad sammanfattning direkt under
rullistan: **`#letter-tally`** (`renderLetterTally()`) räknar hur många
hästar som är märkta med respektive bokstav över hela systemet (alla
avdelningar), t.ex. "8 A-hästar, 0 B-hästar, 0 C-hästar, 0 D-hästar." —
räknar bara markerade hästar, oberoende av om något villkor faktiskt är
aktivt.

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

- `"abc"` (normalläge): `<select>` Ej vald/A/B/C/D, som förut.
- `"plain"`: en enkel `<input type="checkbox">` — internt sätts bokstaven
  `"A"` när ikryssad, precis som om hästen manuellt valts som A i vanligt
  läge. Eftersom villkor samtidigt töms (`rules: []`) blir resultatet hela
  korsprodukten av ikryssade hästar, utan reducering — ingen ändring
  behövdes i `buildCandidates()`/`generateRows()`/export, de bryr sig bara
  om att en bokstav finns satt, inte vilken. Kryssrutans egen `<label>` var
  tidigare statisk ("Ta med {namn}") — nu dynamisk och uppdateras vid varje
  ändring (`updateCheckLabel()`), på uttrycklig begäran: `"Vald {namn}"`
  ikryssad, `"Ej vald {namn}"` avkryssad — samma "Ej vald"-ord som redan
  fanns som alternativ i `<select>`:n för normalläget, nu återanvänt här.
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
på knappen"). Innan alla åtta avdelningar har minst en markerad häst visar
knappen en vägledande text istället ("Markera minst en häst i varje
avdelning …").

**Visuell prominens (byggd efter uttrycklig begäran — knappen "syntes inte"):**
`class="btn-primary"` (samma gula accentfärg som andra viktiga knappar,
t.ex. "Beräkna rader") istället för den vanliga grå standardknappsstilen,
plus egen, något större `font-size`/`padding` (`#btn-sticky-summary` i
CSS). `.sticky-footer` fick också extra `padding-bottom` via
`env(safe-area-inset-bottom, 0px)` (samma mönster som VO Turf List
använder för sina sticky-knappar) så att knappen inte sitter klistrad i
absolut skärmkant utan har lite luft nedåt.

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
- Radpris (0,50 kr) är ett antagande, inte bekräftat direkt mot ATG för V85.
- Spel-id-upptäckt (GitHub Action) ej körd/verifierad över flera dagar än —
  bör observeras några dagar för att bekräfta att den håller sig uppdaterad.
- Ej testat mot en riktig filinlämning på atg.se.
- Ingen engelsk översättning (bara svenska, till skillnad från VO Turf List).

---

## 10. Snabbreferens vid start av ny konversation

1. Läs denna fil
2. Läs `index.html` för att förstå nuläget
3. Fråga vad användaren vill åstadkomma
4. **Diskutera (en fråga i taget) → bekräfta → bygg → verifiera → uppdatera
   tidsstämpel → presentera**
