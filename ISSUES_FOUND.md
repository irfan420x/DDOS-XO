# সমস্যা বিশ্লেষণ (Issues Analysis)

## ১. SecuritySentinel Error: 'LunaGUI' object has no attribute 'activity_log'

**সমস্যার কারণ:**
- `security/security_sentinel.py` ফাইলের ১০৯ লাইনে `self.controller.gui.update_activity()` কল করা হচ্ছে
- কিন্তু `gui/main_window.py` ফাইলে `LunaGUI` ক্লাসে `update_activity()` মেথড আছে, কিন্তু এটি `self.activity_log` অ্যাট্রিবিউট ব্যবহার করে (৩৩৪ লাইন)
- `activity_log` অ্যাট্রিবিউট কখনো তৈরি করা হয়নি - এটি একটি `LiveActivityPanel` দিয়ে প্রতিস্থাপিত হয়েছে (২২১ লাইন)

**সমাধান:**
`gui/main_window.py` ফাইলে `update_activity()` মেথড আপডেট করতে হবে যাতে এটি `self.activity_panel` ব্যবহার করে।

## ২. Invalid icon name "github" in font "fa5s"

**সমস্যার কারণ:**
- `gui/main_window.py` ফাইলের ৭৬ লাইনে `self.create_nav_btn("github", "GitHub")` কল করা হচ্ছে
- `create_nav_btn()` মেথড (২৪৫ লাইন) `fa5s.{icon_name}` ফরম্যাট ব্যবহার করে
- GitHub আইকন Font Awesome Solid (fa5s) তে নেই, এটি Font Awesome Brands (fa5b) তে আছে

**সমাধান:**
`create_nav_btn()` মেথডকে আপডেট করতে হবে যাতে এটি বিভিন্ন আইকন ফন্ট সাপোর্ট করে, অথবা GitHub আইকনের জন্য সঠিক ফন্ট (fa5b.github) ব্যবহার করতে হবে।

## সংক্ষেপ

দুটি প্রধান সমস্যা:
1. **Missing attribute**: `activity_log` অ্যাট্রিবিউট `LunaGUI` ক্লাসে নেই
2. **Wrong icon font**: GitHub আইকন `fa5s` এর পরিবর্তে `fa5b` তে আছে
