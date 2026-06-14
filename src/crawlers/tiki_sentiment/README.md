tiki_sentiment/

├── app/

│ ├── core/
│ │ ├── config.py
│ │ ├── database.py
│ │ └── logger.py
│
│ ├── clients/
│ │ └── tiki_client.py
│
│ ├── models/
│ │ ├── category.py
│ │ ├── product.py
│ │ ├── review.py
│ │ └── crawl_log.py
│
│ ├── repositories/
│ │ ├── category_repository.py
│ │ ├── product_repository.py
│ │ └── review_repository.py
│
│ ├── services/
│ │ ├── category_service.py
│ │ ├── product_service.py
│ │ └── review_service.py
│
│ ├── crawlers/
│ │ ├── category_crawler.py
│ │ ├── product_crawler.py
│ │ └── review_crawler.py
│
│ ├── workers/
│ │ ├── category_worker.py
│ │ ├── product_worker.py
│ │ └── review_worker.py
│
│ └── utils/
│ ├── retry.py
│ ├── time.py
│ └── json.py
│
├── scripts/
│ ├── create_tables.py
│ └── seed_categories.py
│
├── requirements.txt
└── main.py
