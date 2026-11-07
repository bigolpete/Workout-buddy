# LiftLog

A simple workout tracker that runs in the browser. You don't need to install or build anything.

## Run it
- Double-click `index.html`, or
- run `python -m http.server 5173` in this folder and open http://localhost:5173

## On your phone
LiftLog is an installable web app. Host it over HTTPS (GitHub Pages works), open it on the phone, and add it to the home screen:
- **iPhone (Safari):** Share → Add to Home Screen. The installed app has its own storage, separate from Safari, so install before logging (or back up in Safari and import in the app).
- **Android (Chrome):** History → Install, or ⋮ → Install app.

Installed, it opens full screen and works offline (`sw.js` caches the page). It's also protected from Safari's 7-day clearing and can ask Chrome for persistent storage. **History → Keep your data safe** shows the status and has **Back up now**, which opens the share sheet so you can save a backup file to iCloud Drive, Google Drive or email. A reminder appears when you haven't backed up for 2 weeks.

Files: `manifest.webmanifest` (app name, colors, icons), `sw.js` (offline cache, bump `VERSION` when you add files), `icons/` (made by `python tools/make_icons.py`).

## How it works
- **Train**: pick one or more muscle groups and you get suggested lifts: 4 for a single group; on a two-group day 4 for chest, back or legs and 3 for a smaller group; with three or more groups, 3 each (so a third group adds lifts instead of thinning the others). Each lift is 3 sets, so a group gets about 9–12 hard sets, the useful range for one workout. A group gets one extra lift if part of it would otherwise go unworked, and you can add as many as you like. On any lift, **Swap** replaces it with a lift that works the same muscles, preferring different equipment (tap again for the next option). **Choose…** lets you pick any exercise, including ones you create yourself. During the workout you log weight and reps for each set. Each set row shows what you did last time, and the inputs are prefilled with those numbers. When you check off all the sets, the next lift unlocks, and a rest timer starts after each set.
- **Equipment**: adjustable dumbbells and a bench are always assumed. On the Train screen you tick what else you have today (free weight room, cable machines, machines). The plan and Swap only use lifts you can do, and lifts that need other equipment are listed last in the picker. If a group runs short, the plan borrows lifts that work it as a secondary target.
- **Starting weights**: a lift you haven't logged before suggests a first weight. It scales from your other lifts, or from bodyweight and experience (set in History › Settings), and the next set adjusts to the reps you got on set 1.
- **Muscle map**: every lift shows a front/back heatmap of the muscles it works. The plan screen has a **Muscle coverage** card that checks each part of the chosen groups (e.g. upper/mid/lower chest) and suggests a lift for anything missed. It also shows how many sets each group gets today (sets where it's only a helper muscle count half). The auto-plan and the exercise picker all favour lifts that fill gaps.
- **Progress**: per-lift charts (estimated 1RM, heaviest set, volume) and weekly total volume.
- **History**: past workouts, settings (lb/kg, rest timer), and backup export/import.

Data is stored in your browser's localStorage, so use **Export backup** to move it to another device.

## Files
Everything is in `index.html` (styles and scripts are inlined) so it works when opened directly, copied, or emailed as one file. The script blocks are labelled:
- `exercises.js`: exercise library (names, cues, sets/reps, diagram poses)
- `muscles.js`: muscle areas, what each lift works, and the body heatmap
- `figure.js`: animated stick-figure diagrams
- `store.js`: saving data and history queries
- `chart.js`: SVG charts
- `app.js`: screens and workout logic
