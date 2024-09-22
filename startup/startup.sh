# Osx: ~/Library/Application Support/Blender

alias copy_blender_prefs_between_versions='function _copyblenderprefs() { cp /Users/adriano/Library/Application\ Support/Blender/"$1"/config/userpref.blend /Users/adriano/Library/Application\ Support/Blender/"$2"/config; }; _copyblenderprefs'
alias copy_blender_settings_to_repo='function _copyblendersettings() { cp -rf /Users/adriano/Library/Application\ Support/Blender/* /Users/adriano/dev/blender/settings/config/; cp -rf /Users/adriano/Library/Application\ Support/Blender/* /Users/adriano/Soul\ Drive/projects/cg/blender/settings/config/;}; _copyblendersettings'
