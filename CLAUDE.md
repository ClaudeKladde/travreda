# CLAUDE.md — Travreda

Projektinstruktioner för fortsatt utveckling. Läs hela filen innan du börjar.

---

## 1. Om projektet

**Travreda** är en tillgänglighetsanpassad webbapp för att bygga reducerade
travsystem (SK ABC-reducering) för ATG:s spelformer, i första hand **V85**,
byggd specifikt för skärmläsaranvändare (VoiceOver på iPhone i första hand).

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
- **Minimera-knapp:** när detaljvyn expanderas läggs en "Minimera
  {namn}"-knapp till sist i detaljinnehållet, så att man landar på en
  tydlig stängknapp efter att ha svept igenom all information, istället för
  att behöva svepa bakåt till den ursprungliga knappen.

### Sticky avdelningsflikar + meny

Menyknappen (`.menu-wrap`) är `position:absolute` i sticky-radens
övre högra hörn, medvetet borttagen ur flikradens flex-flöde (`.avd-tabs`
har `padding-right` som reserverar plats åt den) — annars konkurrerar
menyknappens bredd med flikarna om utrymmet och tvingar den sista fliken
att radbryta för sig själv. Flikstorleken (`.avd-tab`, ~1,9 rem) är avpassad
för att rymma alla 8 avdelningar på en rad även på en smal mobilskärm.

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
    <!-- en kupong per godkänd rad -->
  </betcoupons>
</issuer>
```

`marks` = 15 tecken, position = startnummer, `1` = markerad. `couponid` är
löpnummer i filen (1–9999 enligt schemat).

**Medvetet enkel modell för v1:** en `<coupon>` per godkänd rad (okomprimerat)
istället för Jokersystemets kupong-komprimering (som packar tusentals rader
till några hundra kuponger via en icke-trivial optimeringsalgoritm). Schemat
tillåter upp till 9999 kuponger, vilket räcker gott för normala
V85-systemstorlekar. Matematiskt identisk insats, bara mindre kompakt fil.
Riktig komprimering kan byggas senare om filerna blir för stora.

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
bokstavsvillkor plus ett sjunde specialläge:

1. Minst 2 A-hästar och max 1 C-häst (**förvalt** — `DEFAULT_PRESET_ID`,
   sätts automatiskt när en ny omgång laddas första gången)
2. Minst 1 A-häst
3. Minst 2 A-hästar
4. Minst 1 A-häst och max 1 C-häst
5. Minst 3 A-hästar och max 1 C-häst
6. Minst 3 A-hästar och max 2 C-hästar
7. **Vanligt matematiskt system utan reducering** (`systemMode = "plain"`)

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

### Vanligt matematiskt system (utan bokstäver)

`systemMode` (`"abc"` | `"plain"`, sparas per omgång i `saveState()`) styr
vilken kontroll som visas per häst i avdelningsvyn:

- `"abc"` (normalläge): `<select>` Ej vald/A/B/C/D, som förut.
- `"plain"`: en enkel `<input type="checkbox">` ("Ta med {namn}") — internt
  sätts bokstaven `"A"` när ikryssad, precis som om hästen manuellt valts
  som A i vanligt läge. Eftersom villkor samtidigt töms (`rules: []`) blir
  resultatet hela korsprodukten av ikryssade hästar, utan reducering —
  ingen ändring behövdes i `buildCandidates()`/`generateRows()`/export,
  de bryr sig bara om att en bokstav finns satt, inte vilken.
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
  × 100` och läggs till direkt efter statusetiketten — exakt den
  uppläsningsordning användaren bad om: `"Vald A-häst, 65% av
  insatsen. 1 Varenne. ..."`. Saknas `liveStats` (inga hästar markerade i
  alla avdelningar än, eller `tooBig`), visas ingen procent alls — bara
  "Vald A-häst." som förut.
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
kr."` — `{X}` är hur många procent som **togs bort** av villkoren
(`100 − (reducerat/oreducerat×100)`), inte hur många som blev kvar. Ett
tryck navigerar till Villkor-vyn (`showView("villkor")`) där samma tal
visas mer utförligt (`#summary-text`, samma `renderLiveSummary()`-funktion
skriver båda). Innan alla åtta avdelningar har minst en markerad häst visar
knappen en vägledande text istället ("Markera minst en häst i varje
avdelning …").

`renderLiveSummary()` är den enda platsen som skriver till
`#btn-sticky-summary`, `#summary-text`, `#calc-status` och togglar
`#btn-export`s `disabled`-status — både den automatiska vägen
(`refreshLiveStatsAndUI`) och den manuella knappen (`btn-calculate`) går
via samma funktion, så de två aldrig kan visa olika/inaktuella tal.

---

## 8. Arkitektur

### Vyer

`view-start` (välj omgång, automatiskt från `data/games.json` eller manuellt
datum+bankod), `view-avdelning` (huvudsidan: sticky avdelningsflikar + meny,
en avdelning i taget: häst/kusk/tränare/procent/barfota + bokstavsval eller
kryssruta), `view-villkor` (villkor, sammanfattning, export),
`view-installningar` (sorteringsval, mer kommer). Enkel vy-växling, ingen
History API ännu (kan läggas till senare om det behövs).

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
uppdaterad text.

**Ej byggt:** inloggning eller serverlagring — bedömdes som en stor
överdrift (kräver backend/databas/autentisering) för ett personligt
verktyg med en användare, och bryter mot enfils/ingen-server-principen.
`localStorage` löser det faktiska problemet (data överlever flikbyte och
hel omladdning) utan den komplexiteten.

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
