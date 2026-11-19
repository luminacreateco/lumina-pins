# Lumina Invites Pinterest automation playbook

Owner: Lumina Invites (Etsy shop LuminaInvites, Pinterest @luminainvites). Owner set this up Nov 18 2026:
pins for new listings as he makes them, plus a drip of existing listings when he isn't producing,
uploaded automatically; "Show shopping recommendations" switched off once pins go live.
Be quiet: only message him if something fails or needs him.

## Where things live
- Repo: github.com/luminacreateco/lumina-pins (images served from raw.githubusercontent.com/.../main/pins/auto/)
- automation/state.json: pin_counts per listing, used_images, new_queue, known_listing_ids, scheduled_through
- automation/build_pins.py: makes 1000x1500 pin JPGs + the bulk CSV from a picks.json
- automation/csv/: every CSV built (name lumina-pins-auto-<first>-<last>.csv)
- Mac copy: ~/Desktop/Lumina Invites/2) Marketing/Claude Pin Automation/ (rename to ...-UPLOADED-... after upload)

## Schedule
- 3 pins a day at 8:00 AM, 2:00 PM, 7:00 PM Pacific. CSV "Publish date" is UTC: in winter (PST, UTC-8) that is
  16:00Z, 22:00Z and 03:00Z the next day; in summer (PDT, UTC-7) 15:00Z, 21:00Z, 02:00Z.
- Each upload run fills every empty slot from the day after scheduled_through up to 7 days ahead of today
  (Pinterest only accepts up to 14 days ahead). If the Mac was asleep and slots were missed, start from tomorrow; never schedule in the past.
- Video pins are NOT in this system (bulk CSV can't take video); the owner posts those by hand.

## Picking pins (in this order)
1. New listings: any listing id in the shop that isn't in known_listing_ids, plus anything in new_queue.
   Up to 2 pins per new listing on its first run (main photo + one scene), spread across different days.
2. Drip: listings with the fewest pin_counts first; break ties by season (winter/holiday themes Nov-Jan,
   Valentine's Jan-Feb, spring/Easter Feb-Apr, pool/summer May-Aug, fall/pumpkin Sep-Oct; birthday themes any time),
   then by best sellers (squishy, mobile+5x7 bundles). Max 1 pin per listing per day, max 2 per listing per run,
   and don't put two pins of the same theme in a row.
3. Photo choice: get the listing's photos from its Etsy page (built-in browser: fetch /listing/<id> and read the
   JSON-LD Product "image" list; space requests ~1 s apart, Etsy rate-limits with 429). Use photos in this order,
   skipping any image id already in used_images: first photo, then the last 4 (scenes, balloons, 5x7 solo).
   Skip the middle text slides (how it works, what you can edit, closing note). Use il_fullxfull URLs.

## Copy rules (the owner's)
- Title <= 100 chars, plain searched words: e.g. "Monster Truck Birthday Invitation for Boys, Red Party Invite, 5x7 Printable".
  Say the format the listing actually is (5x7 printable / mobile text invite + 5x7 / animated video).
- Description <= 500 chars, pain -> fix -> payoff. Open with one approved hook line, rotate them:
  Invites done tonight. Cake tomorrow. / Invites sent. Now the fun part. / Send it tonight. Shop for balloons tomorrow. /
  Invites: done. Goodie bags: next. / One less thing on the list. ✅ / Edited from the soccer bleachers. Sent before the final whistle. /
  Name, date, done, all from your phone. / Changed the name in the car line. Sent before the bell. / Coffee in one hand, invites in the other. /
  The invite they'll want to open again and again. / Make the invite part of the party. / The party starts the moment they open it. /
  Party Saturday? Invites tonight. / Forgot the invites? Send them tonight. / Ten minutes tonight, a party they'll remember. /
  Remembered the cake, forgot the invites? We've got you. / Invites slipped your mind? Send them before bed. /
  No time to design? Just change the name. / Too busy to make invites? Edit one in 10 minutes. / No printer, no problem. Send it from your phone. /
  Skip the print shop. Text it tonight. / Tired of plain invites? Make this one talk. (animated only) / The invite every other parent asks about. /
  Don't send the same invite as everyone else. / "Their face when the squishies start talking. 🥹" = animated squishy only.
  Then what it is + edit on your phone + Canva, a payoff ("Invites ✅" / "Cake tomorrow."), end with "Instant download from Lumina Invites on Etsy."
- Never: "evite" in any spelling, "Monster Jam", trademarked names (Squishmallow, Needoh, Disney etc.), "stress"/"worry",
  "Reuse every year", fake scarcity. Don't reveal the owner's gender; use "we".
- Keywords (Pinterest tags), pick 5-7: always DIY Birthday Invitations, Party Invitations, Kids Birthday Theme, DIY Invitations,
  Kids' Party, Birthday. Add per theme: Boy Birthday Party (boy pins), Sensory Activities (squishy), Neon Party (neon/glow),
  Winter Party / Winter Wonderland Party (winter, incl. Onederland), 1st Birthday (first birthdays, never "First Birthday"),
  2nd Birthday, Pastel. Bundles: DIY Party Decorations, Birthday Games, Party Favors. Baby showers: Baby Shower Invitations, Baby Shower.
- Boards: Squishy Birthday Party Ideas (all squishy), Boy Birthday Party Ideas, Girl Birthday Party Ideas,
  First Birthday Party Ideas (1st birthdays), Neon Glow Party Ideas (glow/neon/disco), Baby Shower Invitations,
  Animated Video Invitations (animated listings), Kids Birthday Games (bundles/games), Kids Birthday Party Invitations (everything else / neutral).

## Upload (built-in browser on the owner's Mac)
1. Push images + CSV to GitHub first and wait until one raw image URL returns 200.
2. Open https://www.pinterest.com/settings/bulk-create-pins, find the file input that accepts .csv, set a File built from the CSV
   text via DataTransfer and dispatch a bubbling 'change' event (same as Nov 13/18). Then click the upload/confirm button if shown.
3. Verify: the page shows the pins processing/created with no error rows. If Pinterest reports errors, fix and retry once.
4. Update state.json (pin_counts, used_images, scheduled_through, last_upload_run), commit + push, and copy the CSV to the Mac pin
   folder with -UPLOADED- in the name.

## Shopping recommendations (daily)
For every created pin that is live: open the pin, "More actions" (find the real ref, never guess coordinates; the next menu item is
the Allow comments toggle) > Edit Pin > More options, switch "Show shopping recommendations" off (#stelaSwitch, or #ShoppingRecSwitch in the
older dialog), Save. Read-only status: PinResource field shopping_rec_disabled. Check every created pin each day, not just new ones
(some flip back on). Never repin or duplicate a pin.
