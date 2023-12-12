from setuptools import setup, find_packages

# Версия вашей библиотеки
version = '0.1.0'

# Длинное описание, которое обычно загружается из файла README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='clickhouse-django-logger',
    version=version,
    author='Алексей',
    author_email='vipzenit666666@gmail.com',
    description='Логгер Django для ClickHouse с интеграцией Celery.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/single-service/clickhouse_django_logger',
    # project_urls={
    #     "Bug Tracker": "URL трекера проблем вашего проекта на GitHub",
    # },
    license='MIT',  # Или другая лицензия, если применимо
    packages=find_packages(exclude=["tests*", "examples*"]),
    include_package_data=True,
    install_requires=[
        'Django>=2.2',
        'celery',
        'requests',
    ],
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
)
