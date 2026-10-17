[app]
title = StudyTimer
package.name = studytimer
package.domain = org.ayush
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,pyjnius==1.9.0
orientation = portrait
fullscreen = 1
android.permissions = WAKE_LOCK
android.archs = arm64-v8a
android.accept_sdk_license = True
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 1
