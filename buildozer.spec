[app]

title = TRIADES
package.name = triades
package.domain = com.croger

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf

requirements = python3,kivy,reportlab

version = 1.0
orientation = portrait
fullscreen = 0

p4a.branch = develop
p4a.source_dir = /home/runner/p4a

android.archs = arm64-v8a
android.minapi = 24
android.api = 36
android.ndk = 29

android.sdk_path = /home/runner/android-sdk
android.accept_sdk_license = True

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE


[buildozer]

log_level = 2
warn_on_root = 1
