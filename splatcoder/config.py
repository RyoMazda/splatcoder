import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class Config(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = '!splatcoder_config'
    build_command: str
    template_path: Optional[str]
    username: Optional[str]
    password: Optional[str]

    @property
    def _template_path(self) -> Path:
        if self.template_path is None:
            return Path('sample_template.cpp')
        else:
            return Path(self.template_path)


def _generate_default_config_file(path: Path) -> None:
    default_config_yml = '''!splatcoder_config
build_command: "g++ -std=c++14"
template_path:
username:
password:
'''
    with open(path, 'w') as f:
        f.write(default_config_yml)


def load() -> Config:
    config_path = Path(os.environ.get('SPLAT_CONFIG_PATH', str(Path.home() / '.splatconfig.yml')))
    if not config_path.exists():
        _generate_default_config_file(config_path)
    with open(config_path) as f:
        config: Config = yaml.safe_load(f)
    return config
