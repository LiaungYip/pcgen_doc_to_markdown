indexes = (
    ( "ability-tag",                           "Data File: abilities.lst",             ),
    ( "abilitycategory-tag",                   "Data File: ability_categories.lst",    ),
    ( "armorproficiencies-tag",                "Data File: armor_proficiencies.lst",   ),
    ( "classes-tag",                           "Data File: classes.lst",               ),
    ( "companionmodifiers-tag",                "Data File: companion_mods.lst",        ),
    ( "deities-tag",                           "Data File: deities.lst",               ),
    ( "domains-tag",                           "Data File: domains.lst",               ),
    ( "equipment-tag",                         "Data File: equipment.lst",             ),
    ( "equipmentmodifiers-tag",                "Data File: equipment_modifiers.lst",   ),
    ( "feats-tag",                             "Data File: feats.lst",                 ),
    ( "install-tag",                           "Data File: install.lst",               ),
    ( "languages-tag",                         "Data File: languages.lst",             ),
    ( "pcc-tag",                               "Data File: campaign.pcc",              ),
    ( "races-tag",                             "Data File: races.lst",                 ),
    ( "shieldproficiencies-tag",               "Data File: shield_proficiencies.lst",  ),
    ( "skills-tag",                            "Data File: skills.lst",                ),
    ( "spells-tag",                            "Data File: spells.lst",                ),
    ( "startingkits-tag",                      "Data File: starting_kits.lst",         ),
    ( "templates-tag",                         "Data File: templates.lst",             ),
    ( "weaponproficiencies-tag",               "Data File: weapon_proficiencies.lst",  ),
    ( "add-tag",                               "Global: ADD",                          ),
    ( "bonus-tag",                             "Global: BONUS",                        ),
    ( "choose-tag",                            "Global: CHOOSE",                       ),
    ( "define-tag",                            "Global: DEFINE",                       ),
    ( "other-tag",                             "Global: OTHER",                        ),
    ( "pre-tag",                               "Global: PRErequisite",                 ),
    ( "gamemode-equipicons-tag",               "Game Mode File: equipicons.lst",       ),
    ( "gamemode-equipmentslots-tag",           "Game Mode File: equipmentslots.lst",   ),
    ( "gamemode-level-tag",                    "Game Mode File: level.lst",            ),
    ( "gamemode-load-tag",                     "Game Mode File: load.lst",             ),
    ( "gamemode-locations-tag",                "Game Mode File: bio/locations.lst",    ),
    ( "gamemode-migration-tag",                "Game Mode File: migration.lst",        ),
    ( "gamemode-miscinfo-tag",                 "Game Mode File: miscinfo.lst",         ),
    ( "gamemode-pointbuymethod-tag",           "Game Mode File: pointbuymethods_system."),
    ( "gamemode-rules-tag",                    "Game Mode File: rules.lst",            ),
    ( "gamemode-statsandchecks-tag",           "Game Mode File: statsandchecks.lst",   ),
    ( "gamemode-tips-tag",                     "Game Mode File: tips.txt",             ),
    ( "biosettings-tag",                       "System File: bio/biosettings.lst",     ),
    ( "sizeadjustment-tag",                    "System File: sizeAdjustment.lst",      ),
    ( "traits-tag",                            "System File: bio/traits.lst",          ),
)

template = """
[[menu.main]]
    name = "{display_name}"
    URL = "/categories/{index_name}.html"
    parent = "tag_indexes"
    weight = {weight}"""

for n, pair in enumerate(indexes):
    index_name, display_name = pair
    weight = 10 * (n+1)
    print (template.format(index_name = index_name, display_name = display_name, weight = weight))
