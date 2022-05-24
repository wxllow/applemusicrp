#!/bin/bash

# Check for python3
if ! [ -x "$(command -v python3)" ]; then
  echo 'Error: python3 could not be found'
  exit 1
fi

# Check for create-dmg
if ! [ -x "$(command -v create-dmg)" ]; then
  echo 'Error: create-dmg could not be found. You can install it with "brew install create-dmg"'
  exit 1
fi

# Check if using universal2 Python
pythonplatform=$(python3 -c "import sysconfig; print(sysconfig.get_platform())")

[[ "$pythonplatform" != *"universal2"* ]] && echo "Warning: You are not using the universal2 version of Python. Builds will not be Universal."

# Build app
echo "Building app..."

cd src/applemusicrp

if python3 setup.py py2app --dist-dir ../../dist/macOS; then
  echo "Building complete."

  # Create DMG
  cd ../../
  echo "Creating DMG..."
  echo "If the DMG open up, just ignore it and wait."
  rm -f dist/AppleMusicRP.dmg

  create-dmg \
    --volname "AppleMusicRP" \
    "dist/AppleMusicRP.dmg" \
    "dist/macOS"
else
  echo "Error: An error occured while building!"
  exit 1
fi
