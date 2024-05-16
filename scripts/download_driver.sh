#!/bin/bash

if [ $# -eq 0 ]
then
  echo "Usage: $0 <browser>"
  echo "<browser> can be 'chrome' or 'firefox'"
  exit 1
fi

download_chromedriver() {
  echo "Downloading ChromeDriver..."
  
  local LATEST_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
  local DOWNLOAD_URL="https://chromedriver.storage.googleapis.com/$LATEST_VERSION/chromedriver_linux64.zip"
  
  wget -qO chromedriver.zip $DOWNLOAD_URL
  unzip -o chromedriver.zip
  rm chromedriver.zip
  chmod +x chromedriver
  echo "ChromeDriver installed successfully."
}

download_geckodriver() {
  echo "Downloading GeckoDriver..."

  local LATEST_VERSION=$(wget -qO- "https://api.github.com/repos/mozilla/geckodriver/releases/latest" | grep 'tag_name' | cut -d '"' -f 4)
  local DOWNLOAD_URL="https://github.com/mozilla/geckodriver/releases/download/$LATEST_VERSION/geckodriver-$LATEST_VERSION-linux64.tar.gz"
  
  wget -qO geckodriver.tar.gz $DOWNLOAD_URL
  tar -xzf geckodriver.tar.gz
  rm geckodriver.tar.gz
  chmod +x geckodriver
  echo "GeckoDriver installed successfully."
}

case $1 in
  chrome)
    download_chromedriver
    ;;
  firefox)
    download_geckodriver
    ;;
  *)
    echo "Unsupported browser: $1"
    echo "Supported browsers are: chrome, firefox"
    exit 1
    ;;
esac
