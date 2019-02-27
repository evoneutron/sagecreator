import yaml
import sys
import logging
import base64

logging.basicConfig(level=logging.INFO, format='%(name)-12s: %(levelname)-8s: %(message)s')
log = logging.getLogger(__name__)

from pathlib import Path


class Configurator:

    def __init__(self):
        site_packages = next(p for p in sys.path if 'site-packages' in p)
        self._root_path = "{}/sagebase".format(site_packages)

    def persist(self, access_key_id, secret_access_key, company, owner, service, instance_type, spot_price, cluster_size, private_key_file):
        config = {'aws_access_key': access_key_id,
                  'aws_secret_key': base64.b64encode(secret_access_key.encode("utf-8")),
                  'company': company,
                  'owner': owner,
                  'service': service,
                  'instance_type': instance_type,
                  'spot_price': spot_price,
                  'cluster_size': cluster_size}
        if private_key_file:
            config.update({'private_key_file': private_key_file})
        template = self._read_template()
        template.update(config)
        with open(self.get_config_path(), "w") as infile:
            infile.write(yaml.safe_dump(template, default_flow_style=False))

    def _read_template(self):
        file_path = Path("{}/templates/{}".format(self.get_root_path(), "config.yml"))
        if not file_path.exists():
            raise ValueError("Template file with default configuration settings could not be read")

        with open(str(file_path), "r") as stream:
            template = yaml.load(stream)
        return template

    def get_properties(self):
        with open(self.get_config_path(), "r") as stream:
            props = yaml.load(stream)
        return props

    def get_config_path(self):
        return "{}/inventory/stage/group_vars/all/{}".format(self._root_path, "config.yml")

    def get_root_path(self):
        return self._root_path

    def get_valid_instance_types(self):
        valid_types_path = "{}/inventory/stage/group_vars/all/{}".format(self._root_path, "valid_instance_types.yml")
        with open(str(valid_types_path), "r") as stream:
            props = yaml.load(stream)
        return props.get("valid_instance_types")