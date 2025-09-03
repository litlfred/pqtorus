#!/bin/bash

# Test script to validate Capacitor configuration and Android setup
# Run this from the web/ directory

set -e

echo "🧪 Testing PQTorus Android Configuration..."
echo ""

# Check if we're in the correct directory
if [ ! -f "capacitor.config.ts" ]; then
    echo "❌ Error: capacitor.config.ts not found. Run from web/ directory."
    exit 1
fi

# Test 1: Verify Capacitor config
echo "1️⃣  Testing Capacitor configuration..."
npx cap config > /dev/null
echo "✅ Capacitor config is valid"

# Test 2: Check if Android platform is added
echo "2️⃣  Checking Android platform..."
if [ ! -d "android" ]; then
    echo "❌ Android platform not found"
    exit 1
fi
echo "✅ Android platform exists"

# Test 3: Verify web build works
echo "3️⃣  Testing web build..."
npm run build > /dev/null
echo "✅ Web build successful"

# Test 4: Test Capacitor sync
echo "4️⃣  Testing Capacitor sync..."
npx cap sync android > /dev/null
echo "✅ Capacitor sync successful"

# Test 5: Verify assets are copied
echo "5️⃣  Verifying Android assets..."
if [ ! -f "android/app/src/main/assets/public/index.html" ]; then
    echo "❌ Web assets not found in Android project"
    exit 1
fi
echo "✅ Web assets properly copied to Android project"

# Test 6: Check Android manifest
echo "6️⃣  Checking Android manifest..."
if [ ! -f "android/app/src/main/AndroidManifest.xml" ]; then
    echo "❌ Android manifest not found"
    exit 1
fi
echo "✅ Android manifest exists"

# Test 7: Verify Gradle wrapper
echo "7️⃣  Checking Gradle wrapper..."
if [ ! -f "android/gradlew" ]; then
    echo "❌ Gradle wrapper not found"
    exit 1
fi
if [ ! -x "android/gradlew" ]; then
    echo "🔧 Making gradlew executable..."
    chmod +x android/gradlew
fi
echo "✅ Gradle wrapper is ready"

echo ""
echo "🎉 All tests passed! Android configuration is valid."
echo ""
echo "Next steps:"
echo "- Run './build-android.sh' to build the APK"
echo "- Or use 'npm run android:build' for debug APK"
echo "- Check GitHub Actions for automated builds"