# Connection Limiter

Discord bot koji ograničava broj korisnika koji se istovremeno mogu povezati na glasovne (voice) kanale na serveru.

## O projektu

Bot prati aktivnost korisnika na glasovnim kanalima i automatski ograničava ukupan broj konekcija, u skladu sa zadanim pravilima. Napisan je u Pythonu koristeći Discord bot biblioteku, sa jasno odvojenom strukturom za event handlere, pomoćne funkcije i pozadinske zadatke (tasks).

## Struktura projekta

- `bot.py` — glavna ulazna tačka bota
- `event_handlers/` — logika za reagovanje na Discord evente (npr. spajanje/napuštanje glasovnog kanala)
- `helpers/` — pomoćne funkcije
- `tasks/` — pozadinski (scheduled) zadaci
- `requirements.txt` — Python zavisnosti

## Pokretanje

```bash
git clone https://github.com/denissofovic/connection-limiter.git
cd connection-limiter
pip install -r requirements.txt
python bot.py
```

Potrebno je kreirati Discord bot aplikaciju preko [Discord Developer Portal](https://discord.com/developers/applications) i postaviti bot token (npr. kao environment varijablu) prije pokretanja.

## Autor

Denis Sofović
