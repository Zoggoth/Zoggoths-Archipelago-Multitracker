# Zoggoth's Archipelago Multitracker

A tool for combining multiple [Archipelago](https://archipelago.gg/) trackers into one list.  
Intended for large asyncs, where a user might get multiple items across multiple games overnight, and need a list of which are important

## Usage

Put all trackers in "Tracker List.txt" with the format "GameName: TrackerLink"  
Run main.py  

### Troubleshooting

The first run will print all items (since it doesn't know when you last checked each world).  
All subsequent runs will remember when you last checked & only print new items

If the game has a specialised tracker (e.g Super Metroid, Ocarina of Time), make sure to use a link to the generic tracker

The GameName should be the same format as the names in the worlds folder (e.g "Ocarina of Time" rather than "TLoZ: OOT").  
These generally match the names used by the existing multi-world tracker

If the game/item isn't in the worlds folder, it will be marked as unknown.  
You will still be told which items are new, but will have to work out yourself which items are important

## To Do

Split progression into Macguffins & progression.  
Macguffins are sometimes a large section of the item pool (120 stars in SM64, 180+ emblems in SA2B) & can distract from more important progression like level unlocks

ADD MORE GAMES!  
All game currently work, but if you want to split a new game into progression/useful/filler, then I'd be happy to help!  
Ideally I want it to work with all supported games + as many unsupported/manual as possible