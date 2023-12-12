from setuptools import find_packages, setup

long_desc = open("README.md").read()

setup(
    name="django-powcaptcha",
    version="0.0.1",
    description="Django PowCaptcha form field/widget app.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author="Jean-Philippe Bidegain",
    author_email="jp@bidega.in",
    license="BSD",
    url="https://github.com/aeyoll/django-powcaptcha",
    project_urls={
        "Changelog": "https://github.com/aeyoll/django-powcaptcha/blob/main/CHANGELOG.md",
        "Issue Tracker": "https://github.com/aeyoll/django-powcaptcha/issues",
    },
    packages=find_packages(),
    install_requires=["django"],
    keywords=["django", "powcaptcha"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    zip_safe=False,
)
