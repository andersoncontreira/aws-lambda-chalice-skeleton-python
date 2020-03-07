cp .env.example .env
python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements-vendor.txt -t ./vendor
python3 -m pip install -r requirements-chalice.txt
