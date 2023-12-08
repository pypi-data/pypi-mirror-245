import pathlib
import setuptools

setuptools.setup(
    name="autopilotml",
    version="1.0.6",
    keywords=["autopilotml",'machine learning', 'data science', 'automated machine learning', 'regressor', 'regressors', 'regression', 'classification', 'classifiers', 'classifier', 'estimators', 'predictors', 'XGBoost', 'Random Forest', 'sklearn', 'scikit-learn', 'analytics', 'analysts', 'coefficients', 'feature importances' 'analytics', 'artificial intelligence', 'subpredictors', 'ensembling', 'stacking', 'blending', 'feature engineering', 'feature extraction', 'feature selection', 'production', 'pandas', 'dataframes', 'machinejs', 'deep learning', 'tensorflow', 'deeplearning', 'lightgbm', 'gradient boosting', 'gbm', 'keras', 'production ready', 'test coverage'],
    author="Shyam Prasath",
    author_email="shshyam96@gmail.com",
    description="A package for automating machine learning tasks",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/shyam1326",
    packages=setuptools.find_packages(),
    include_package_data=True,
    license="MIT",
    project_urls={
        "Source": "https://github.com/shyam1326/autopilotml",
        "Bug Reports": "https://github.com/shyam1326/autopilotml/issues",
        "Documentation": "https://github.com/shyam1326/autopilotml/blob/main/README.md",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8, <3.12",
    install_requires=[requirement.strip() for requirement in pathlib.Path("requirements.txt").read_text().splitlines()],
    entry_points={
        "console_scripts": [
            "autopilotml=autopilotml.__main__:autopilotml",
        ],
    },
    

)
