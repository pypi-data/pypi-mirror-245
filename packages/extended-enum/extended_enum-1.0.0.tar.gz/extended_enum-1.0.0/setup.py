# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['extended_enum']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'extended-enum',
    'version': '1.0.0',
    'description': 'Extends the capabilities of the standard Enum.',
    'long_description': '# python-extended-enum\n\n## Introduction\n\nPackage that expands the capabilities of the standard Enum.\n\n## Features\n\n- store additional information inside Enum member\n\n## Install\n\n```shell\npip install python-extended-enum\n```\n\n## Usage\n\n### Quick Start\n\n```python\nfrom dataclasses import dataclass, field\nfrom enum import unique\nfrom typing import Optional\nfrom uuid import UUID\nfrom extended_enum import ExtendedEnum, ValueWithDescription, BaseExtendedEnumValue\n\n\n@dataclass(frozen=True)\nclass SomeExtendedEnumValue(BaseExtendedEnumValue):\n    display_name: str = field(compare=False)\n    description: Optional[str] = field(default=None, compare=False)\n    \n\nclass MixedEnum(ExtendedEnum):\n    """A combined enumeration in which member values are of different types."""\n    CONST1 = \'const1\'\n    CONST2 = 1\n    CONST3 = UUID(\'79ff3431-3e98-4bec-9a4c-63ede2580f83\')\n    NOT_DUPLICATE_CONST3 = \'79ff3431-3e98-4bec-9a4c-63ede2580f83\'\n    CONST4 = BaseExtendedEnumValue(value=\'const4\')\n    CONST5 = BaseExtendedEnumValue(value=2)\n    CONST6 = BaseExtendedEnumValue(value=UUID(\'e7b4b8ae-2224-47ec-afce-40aeb10b85e2\'))\n    CONST7 = ValueWithDescription(value=\'const7\')\n    CONST8 = ValueWithDescription(value=3, description=\'some const8 description\')\n    CONST9 = SomeExtendedEnumValue(value=\'const9\', display_name=\'some display name\', description=\'some const9 description\')\n\nunique(MixedEnum)\n```\n\n```pycon\n>>> MixedEnum.CONST9\n<MixedEnum.CONST9: SomeExtendedEnumValue(value=\'const9\', display_name=\'some display name\', description=\'some const9 description\')>\n>>> MixedEnum.CONST9.value\n\'const9\'\n>>> MixedEnum.CONST9.extended_value\nSomeExtendedEnumValue(value=\'const9\', display_name=\'some display name\', description=\'some const9 description\')\n>>> MixedEnum.get_values()\nTuple \n(\'const1\',\n 1,\n UUID(\'79ff3431-3e98-4bec-9a4c-63ede2580f83\'),\n \'79ff3431-3e98-4bec-9a4c-63ede2580f83\',\n \'const4\',\n 2,\n UUID(\'e7b4b8ae-2224-47ec-afce-40aeb10b85e2\'),\n \'const7\',\n 3,\n \'const9\')\n>>> MixedEnum.get_extended_values()\nTuple \n(BaseExtendedEnumValue(value=\'const1\'),\n BaseExtendedEnumValue(value=1),\n BaseExtendedEnumValue(value=UUID(\'79ff3431-3e98-4bec-9a4c-63ede2580f83\')),\n BaseExtendedEnumValue(value=\'79ff3431-3e98-4bec-9a4c-63ede2580f83\'),\n BaseExtendedEnumValue(value=\'const4\'),\n BaseExtendedEnumValue(value=2),\n BaseExtendedEnumValue(value=UUID(\'e7b4b8ae-2224-47ec-afce-40aeb10b85e2\')),\n ValueWithDescription(value=\'const7\', description=None),\n ValueWithDescription(value=3, description=\'some const8 description\'),\n SomeExtendedEnumValue(value=\'const9\', display_name=\'some display name\', description=\'some const9 description\'))\n```\n\n## License\n\nThis project is licensed under the [Apache-2.0](https://github.com/ilichev-andrey/python-extended-enum/blob/master/LICENSE) License.\n',
    'author': 'Ilichev Andrey',
    'author_email': 'ilichev.andrey.y@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
