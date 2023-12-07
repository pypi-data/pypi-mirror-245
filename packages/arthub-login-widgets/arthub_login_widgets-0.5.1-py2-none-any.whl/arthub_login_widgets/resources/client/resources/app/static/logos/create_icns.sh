sips -z 16 16     10241024.png --out tmp.iconset/icon_16x16.png
sips -z 32 32     10241024.png --out tmp.iconset/icon_16x16@2x.png
sips -z 32 32     10241024.png --out tmp.iconset/icon_32x32.png
sips -z 64 64     10241024.png --out tmp.iconset/icon_32x32@2x.png
sips -z 128 128   10241024.png --out tmp.iconset/icon_128x128.png
sips -z 256 256   10241024.png --out tmp.iconset/icon_128x128@2x.png
sips -z 256 256   10241024.png --out tmp.iconset/icon_256x256.png
sips -z 512 512   10241024.png --out tmp.iconset/icon_256x256@2x.png
sips -z 512 512   10241024.png --out tmp.iconset/icon_512x512.png
sips -z 1024 1024   10241024.png --out tmp.iconset/icon_512x512@2x.png
iconutil -c icns tmp.iconset -o icon-logo.icns