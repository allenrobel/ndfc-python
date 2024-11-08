#!/usr/bin/env python
"""
Name: util/make_markdown.py
Summary: Generate markdown from an NDFC template

Used to help generate the markdown files in docs/*

cp $HOME/repos/ansible_dev/ndfc_doc_builder/docs/isn.yaml /tmp
cp $HOME/repos/ansible_dev/ndfc_doc_builder/docs/lan-classic.yaml /tmp
cp $HOME/repos/ansible_dev/ndfc_doc_builder/docs/msd.yaml /tmp
cp $HOME/repos/ansible_dev/ndfc_doc_builder/docs/vxlan-evpn.yaml /tmp
./util/make_markdown.py
cp /tmp/isn.md $HOME/repos/dcnm-docpoc/docs/modules/dcnm_fabric/isn.md
cp /tmp/lan-classic.md $HOME/repos/dcnm-docpoc/docs/modules/dcnm_fabric/lan-classic.md
cp /tmp/msd.md $HOME/repos/dcnm-docpoc/docs/modules/dcnm_fabric/msd.md
cp /tmp/vxlan-evpn.md $HOME/repos/dcnm-docpoc/docs/modules/dcnm_fabric/vxlan-evpn.md

"""
from ndfc_python.util.markdown_from_template import MarkdownFromTemplate

for file in ["isn.yaml", "lan-classic.yaml", "msd.yaml", "vxlan-evpn.yaml"]:
    instance = MarkdownFromTemplate()
    instance.template_file = f"/tmp/{file}"
    instance.markdown_file = f"/tmp/{file.replace('.yaml', '.md')}"
    instance.commit()
# instance = MarkdownFromTemplate()
# instance.template_file = "/tmp/vxlan-evpn.yaml"
# instance.markdown_file = "/tmp/vxlan-evpn.md"
# # instance.property_map_file = "./default_network_universal_property_map.yaml"
# instance.commit()
