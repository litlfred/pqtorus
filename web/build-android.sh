#!/bin/bash

# PQTorus Android Build Script
# This script builds the Android APK for the PQTorus web application

set -e

echo "🚀 Building PQTorus Android APK..."
echo ""

# Check if we're in the correct directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: This script must be run from the web/ directory"
    exit 1
fi

# Check if Android project exists
if [ ! -d "android" ]; then
    echo "❌ Error: Android project not found. Run 'npx cap add android' first."
    exit 1
fi

echo "📦 Installing dependencies..."
npm install

echo "🔨 Building web application..."
npm run build

echo "🔄 Syncing with Capacitor..."
npx cap sync android

echo "🏗️  Building Android APK..."
cd android

# Check for Java
if ! command -v java &> /dev/null; then
    echo "❌ Error: Java is required but not installed."
    echo "Please install Java 17+ and try again."
    exit 1
fi

# Build debug APK
echo "Building debug APK..."
./gradlew assembleDebug

echo ""
echo "✅ Build completed successfully!"
echo ""
echo "📱 APK Location:"
echo "   Debug: android/app/build/outputs/apk/debug/app-debug.apk"
echo ""
echo "To install on a connected device:"
echo "   adb install android/app/build/outputs/apk/debug/app-debug.apk"
echo ""
echo "To build a release APK (unsigned):"
echo "   ./gradlew assembleRelease"
echo "   Location: android/app/build/outputs/apk/release/app-release-unsigned.apk"