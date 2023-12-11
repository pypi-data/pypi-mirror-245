# python setup.py sdist bdist_wheel  # 打包项目
# python -m twine upload dist/*  # 上传项目

# __init__.py 的 __version__
# setup.py 的 Version
# CHANGELOG.md
# README.md
# 兼容性测试
# 跨平台测试

import setuptools

kw_args = {
    'name': 'tkintertools',  # 包名称
    'version': '2.6.18',  # 包版本（必须比上次的大）
    'description': 'The tkintertools module is an auxiliary module of the tkinter module.',  # 简明描述
    # 长描述（此处直接使用自述文件）
    'long_description': open('README.md', encoding="utf-8").read(),
    'long_description_content_type': 'text/markdown',  # 长描述的文件类型（此处为文本或 Markdown 文件）
    'author': 'Xiaokang2022',  # 作者
    'author_email': '2951256653@qq.com',  # 作者邮箱
    'maintainer': 'Xiaokang2022',  # 维护者
    'maintainer_email': '2951256653@qq.com',  # 维护者邮箱
    'url': 'https://github.com/Xiaokang2022/tkintertools',  # 包的源代码仓库地址
    'license': 'MulanPSL-2.0',  # 项目许可证
    'python_requires': '>=3.8',  # 包的 Python 要求（自己设定）
    'packages': [  # 包的内容（含 __init__.py 的文件夹）
        'tkintertools',
    ],
    'keywords': [  # 包的关键词（方便别人搜索和查找）
        'tkinter',
        'tkintertools',
        'GUI',
        'tools',
    ],
    'classifiers': [  # 验证信息
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)',
        'Operating System :: OS Independent',
    ],
}

setuptools.setup(**kw_args)

# pypistats overall tkintertools
# pypistats recent tkintertools
# pypistats system tkintertools
# pypistats python_minor tkintertools
# pypistats python_major tkintertools
