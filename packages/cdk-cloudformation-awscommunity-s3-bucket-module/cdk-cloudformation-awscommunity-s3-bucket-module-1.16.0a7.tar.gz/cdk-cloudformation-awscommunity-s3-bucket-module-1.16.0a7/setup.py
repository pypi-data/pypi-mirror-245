import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-cloudformation-awscommunity-s3-bucket-module",
    "version": "1.16.0.a7",
    "description": "Schema for Module Fragment of type AwsCommunity::S3::Bucket::MODULE",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs/cdk-cloudformation.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/cdk-cloudformation.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_cloudformation_awscommunity_s3_bucket_module",
        "cdk_cloudformation_awscommunity_s3_bucket_module._jsii"
    ],
    "package_data": {
        "cdk_cloudformation_awscommunity_s3_bucket_module._jsii": [
            "awscommunity-s3-bucket-module@1.16.0-alpha.7.jsii.tgz"
        ],
        "cdk_cloudformation_awscommunity_s3_bucket_module": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.114.1, <3.0.0",
        "constructs>=10.3.0, <11.0.0",
        "jsii>=1.93.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
