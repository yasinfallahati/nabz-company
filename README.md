# شرکت مجازی نبض فردا

داشبورد تیم بات‌های «نبض فردا». **By Yasin**

## به‌روزرسانی داده‌ها
فایل‌های `data/` را ویرایش و به `main` کامیت کنید؛ GitHub Pages خودکار دوباره منتشر می‌کند.
- `data/company.json`: اعضا (`people`، فیلد `reports` = مدیر بالادست) و پروژه‌ها (`projects`)
- `data/meetings.json`: جلسه‌ها (`brief`، `inputs[{who,text}]`، `plan[]`)
- `data/tasks.json`: کارها (`status`: todo | doing | approval | done، `owner`، `project`) و `activity`

## دفتر سه‌بعدی
صفحه اصلی (`index.html`) دفتر سه‌بعدی است و هر ۵ ثانیه `data/live.json` را می‌خواند؛ داشبورد قدیمی در `dashboard.html`.
به‌روزرسانی: `python3 scripts/update_live.py --help` (نیازمند `NABZ_GITHUB_TOKEN`).
