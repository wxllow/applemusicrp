#!/bin/bash
 
# Check for create-dmg
if ! [ -x "$(command -v create-dmg)" ]; then
  echo 'Error: create-dmg could not be found. You can install it with "brew install create-dmg"' >&2
  exit 1
fi

echo "Building app..."
python3 setup.py py2app --dist-dir "dist/macOS"
echo "Building complete."

echo "Creating DMG..."
echo "If the DMG opens up, just close it out."
rm -f dist/AppleMusicRP.dmg
create-dmg \
    --volname "AppleMusicRP" \
    "dist/AppleMusicRP.dmg" \
    "dist/macOS/" 