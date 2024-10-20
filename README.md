# blender
https://github.com/paulgolter/blender-pipeline-integration?tab=readme-ov-file

# User Directories
https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html#blender-directory-layout

# macOS
/Users/$USER/Library/Application Support/Blender/4.2/

# Windows
%USERPROFILE%\AppData\Roaming\Blender Foundation\Blender\4.2\


# Custom Env
blender:
> import sys

> print(sys.executable)

shell:
> /Applications/Blender.app/Contents/Resources/4.2/python/bin/python3.11 -m venv venv

> export PYTHONPATH="$PYTHONPATH:/Users/$USER/dev/blender/venv/lib/python3.11/site-packages"; blender --python-use-system-env;
