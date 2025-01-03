# Zoggoth's Archipelago Multitracker

A tool for combining multiple [Archipelago](https://archipelago.gg/) trackers into one list.  
Intended for large asyncs, where a user might get multiple items across multiple games overnight, and need a list of which are important

## Usage

Put game names & tracker links into "Tracker List.txt" (see [Tracker List.txt](https://github.com/Zoggoth/Zoggoths-Archipelago-Multitracker/blob/main/Tracker%20List.txt) for an example)  
Run main.exe  
If tracking large numbers of slots, "generate tracker list.exe" can be used to extract multiple tracking links from an archipelago room

Tracker List.txt supports various formats:  
* "Pokemon Emerald: https..."  
* "Pokemon Emerald (Zoggoth_Emerald): https..."  
* "(Zoggoth_Emerald): https..."  
* "https..."

All 4 will show new items, but the game name is needed to sort items into progression/useful/filler  

## Troubleshooting

The first run will print all items (since it doesn't know when you last checked each world).  
All subsequent runs will remember when you last checked & only print new items

The GameName should be the same format as the names in the worlds folder (e.g "Ocarina of Time" rather than "TLoZ: OOT").  
These generally match the names used by the existing multi-world tracker

If the game/item isn't in the worlds folder, it will be marked as unknown.  
You will still be told which items are new, but will have to work out yourself which items are important

## To Do

Split progression into Macguffins & progression.  
Macguffins are sometimes a large section of the item pool (120 stars in SM64, 180+ emblems in SA2B) & can distract from more important progression like level unlocks

ADD MORE GAMES!  
All games display received items, but they need progression/useful/filler info to work fully  
Some progression info can be extracted from the Archipelago logic files, but edge cases might need someone familiar with the game to help  
If you have experience in a game that isn't tracked yet, or have corrections for a game that's already tracked, please let me know  
Ideally I want progression info for all supported games + as many unsupported/manual as possible  
All 0.5.1 supported are done except: Factorio, The Messenger, Stardew Valley, Terraria, Yu-Gi-Oh! 2006, Zillion