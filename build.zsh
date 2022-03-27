#!/bin/zsh

# Check for create-dmg
if ! [ -x "$(command -v create-dmg)" ]; then
  echo 'Error: create-dmg could not be found. You can install it with "brew install create-dmg"'
  exit 1
fi

# Check architecture
if [ "$(uname -m)" = "x86_64" ]; then
  echo 'Warning: You are using an Intel Mac (or using Rosetta).'
fi

echo "Building app..."

python3 setup.py py2app --dist-dir "dist/macOS"

echo "Building complete."

echo "Creating DMG..."
echo "If the DMG open up, just ignore it and wait."
rm -f dist/AppleMusicRP.dmg

create-dmg \
  --volname "AppleMusicRP" \
  "dist/AppleMusicRP.dmg" \
  "dist/macOS"
