#!/usr/bin/env python
"""
Name: util/make_markdown.py
Summary: Generate markdown from an NDFC template

Used to help generate the markdown files in docs/*
"""
from ndfc_python.util.markdown_from_template import MarkdownFromTemplate

instance = MarkdownFromTemplate()
instance.template_file = "/tmp/default_network_universal.yaml"
instance.markdown_file = "/tmp/default_network_universal.md"
instance.property_map_file = "./default_network_universal_property_map.yaml"
instance.commit()
