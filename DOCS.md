# Problēmas izpēte un analīze
Mūsdienu programmētāji un studenti bieži vien vēlas ātri kopīgot koda fragmentus vai tekstu ar citiem, neizmantojot sarežģītus rīkus. Šī projekta mērķis ir nodrošināt vienkāršu tīmekļa lietotni teksta fragmentu glabāšanai un kopīgošanai-- līdzīgi kā `pastebin.com`. Mērķauditorija ir programmētāji un tehniski lietotāji, kuriem nepieciešams ātrs veids, kā kopīgot tekstu.
Mērķauditorija neaprobežojas tikai ar programmētājiem un studentiem. Tā kā šis ir daudzfunkcionāls rīks, to var izmantot ikviens, kam ir nepieciešams dalīties ar teksta saturu internetā.
# Programmatūras prasību specifikācija
## Funkcionālās prasības:

Lietotājs var reģistrēties un pieteikties sistēmā.
Autentificēts lietotājs var izveidot, rediģēt un dzēst savus teksta fragmentus (notes).
Administrators var dzēst jebkuru note un jebkuru lietotāju.
Visi apmeklētāji (arī nereģistrēti) var skatīt publicētās notes.
Sistēma nodrošina divu līmeņu piekļuvi: parasts lietotājs (user) un administrators (admin).

## Nefunkcionālās prasības:

Lietotne darbojas lokāli uz jebkura datora ar Python 3.
Paroles tiek glabātas hašētas lai nodrošināt kontes drošība.
Lietotne reaģē uz pieprasījumiem mazāk nekā 1 sekundē lokālā vidē.


# Programmatūras dizains
Izstrādē tika izmantots Python ar Flask mikro-ietvaru, jo tas ir viegls, plaši izmantots un piemērots mazām tīmekļa lietotnēm. Datu glabāšanai izvēlēts SQLite-- tas nevēlas atsevišķa servera un ir ideāls vienkāršiem projektiem. Veidnes tiek renderētas ar Jinja2 (iebūvēts Flask).
Sistēma sastāv no trim galvenajiem moduļiem:

models.py-- User un Note klases ar metodēm (is_admin(), preview()).
database.py-- Database klase, kas veic visas SQLite operācijas un uztur dict tipa kešatmiņu pastēm.
app.py-- Flask maršruti autentifikācijai, pastu CRUD operācijām un administrācijai.

ER modelis:
`users` tabula: `username` (PK), `password`, `role`.
`notes` tabula: `id` (PK), `title`, `content`, `author` (FK -> `users.username`), `created_at`.

# Programmatūras izstrādes plāns
Projektam tika izvēlēts ūdenskrituma (Waterfall) modelis, jo prasības bija skaidri definētas jau sākumā un projekts ir neliels. Iteratīva pieeja šādā gadījumā būtu pārmērīgi sarežģīta.
Izstrādes posmi:

1. Prasību definēšana un sistēmas projektēšana.
2. Datu bāzes shēmas izveide.
3. Modeļu un datu bāzes klases izstrāde.
4. Flask maršrutu un veidņu izstrāde.
5. Testēšana un kļūdu labošana.


# Atkļūdošana un pieņemšanas testēšana
Atkļūdošana tika veikta manuāli, izmantojot Flask iebūvēto debug=True režīmu, kas parāda detalizētas kļūdu izvadnes pārlūkprogrammā. Tika pārbaudīti šādi scenāriji:

Reģistrācija ar jau esošu lietotājvārdu-- parāda kļūdas ziņojumu.
Pieteikšanās ar nepareizu paroli-- piekļuve tiek liegta.
Notes rediģēšana/dzēšana, nepiederoties tai-- piekļuve tiek liegta.
Administrators var dzēst jebkuru lietotāju un note.
Nereģistrēts lietotājs var skatīt notes, bet nevar tās veidot.

Pieņemšanas testēšana tika veikta, manuāli izejot cauri visiem lietotāja scenārijiem pārlūkprogrammā.

# Lietotāja rokasgrāmata
Instalācija:
Nepieciešams Python 3.8+. Lejupielādējiet projekta failus un izpildiet:
`python3 -m venv venv`
`source venv/bin/activate`
`pip install flask`
`python app.py`

Atveriet pārlūkprogrammā: http://127.0.0.1:5000

Lietošana:

Reģistrācija: Spiediet "Register", ievadiet lietotājvārdu un paroli. Pēc reģistrācijas piesakieties ar tiem pašiem datiem.

Notes izveide: Pēc pieteikšanās spiediet "New Note", ievadiet virsrakstu un saturu, spiediet "Create Note".

Rediģēšana/dzēšana: Atveriet savu note un spiediet "Edit" vai "Delete". Dzēšana prasa apstiprinājumu.

Administrators: Noklusējuma administrators - lietotājvārds `admin`, parole `admin`. Administrators var piekļūt "Admin Panel", kur iespējams dzēst lietotājus.


