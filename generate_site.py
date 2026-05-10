#!/usr/bin/env python3
"""
Static Site Generator using Jinja2 templates
"""
import json
import os
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class StaticSiteGenerator:
    def __init__(self, templates_dir='templates', data_dir='data',
                 static_dir='static', output_dir='output'):
        """
        Initialize the static site generator.

        Args:
            templates_dir: Directory containing Jinja2 templates
            data_dir: Directory containing JSON data files
            static_dir: Directory containing static assets (CSS, images, etc.)
            output_dir: Directory where generated site will be output
        """
        self.templates_dir = Path(templates_dir)
        self.data_dir = Path(data_dir)
        self.static_dir = Path(static_dir)
        self.output_dir = Path(output_dir)

        # Setup Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=True
        )

    def load_json_data(self, filename):
        """Load JSON data from the data directory."""
        filepath = self.data_dir / filename
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def render_template(self, template_name, data):
        """Render a Jinja2 template with the provided data."""
        template = self.env.get_template(template_name)
        return template.render(**data)

    def copy_static_files(self):
        """Copy static files (CSS, images, etc.) to output directory."""
        if self.static_dir.exists():
            output_static = self.output_dir / 'static'
            if output_static.exists():
                shutil.rmtree(output_static)
            shutil.copytree(self.static_dir, output_static)
            print(f"Copied static files to {output_static}")

    def load_person_by_slug(self, slug):
        """Load a person's data from data/people/{slug}.json"""
        try:
            person_file = f"people/{slug}.json"
            person_data = self.load_json_data(person_file)
            person_data['slug'] = slug
            return person_data
        except Exception as e:
            print(f"Warning: Could not load person '{slug}': {e}")
            return None

    def load_all_people(self):
        """Load all people from data/people directory."""
        people = []
        people_dir = self.data_dir / 'people'

        if people_dir.exists():
            for json_file in people_dir.glob('*.json'):
                slug = json_file.stem
                person_data = self.load_person_by_slug(slug)
                if person_data:
                    people.append(person_data)

        return people

    def hydrate_person_references(self, data):
        """
        Hydrate person references in the data.
        Looks for 'recent_additions.featured' and 'recent_additions.others'
        and loads full person data from people/*.json files.
        """
        if 'recent_additions' in data:
            # Hydrate featured person
            if 'featured' in data['recent_additions']:
                ref = data['recent_additions']['featured']
                if isinstance(ref, dict) and 'slug' in ref:
                    person_data = self.load_person_by_slug(ref['slug'])
                    if person_data:
                        data['recent_additions']['featured'] = person_data

            # Hydrate others list
            if 'others' in data['recent_additions']:
                hydrated_others = []
                for ref in data['recent_additions']['others']:
                    if isinstance(ref, dict) and 'slug' in ref:
                        person_data = self.load_person_by_slug(ref['slug'])
                        if person_data:
                            hydrated_others.append(person_data)
                    else:
                        hydrated_others.append(ref)
                data['recent_additions']['others'] = hydrated_others

        return data

    def generate_page(self, template_name, data_file, output_file):
        """
        Generate a single page.

        Args:
            template_name: Name of the template file
            data_file: Name of the JSON data file (can be None for archive)
            output_file: Path to output HTML file (relative to output_dir)
        """
        # Special handling for archive template
        if template_name == 'archive.html':
            data = {'people': self.load_all_people()}
        else:
            # Load data
            data = self.load_json_data(data_file)

            # Hydrate person references for home template
            if template_name == 'home.html':
                data = self.hydrate_person_references(data)
                # Add people count for "See all X" link
                data['people'] = self.load_all_people()

            # Wrap person data if using person template
            if template_name == 'person.html':
                data = {'person': data}

        # Render template
        html = self.render_template(template_name, data)

        # Write output
        output_path = self.output_dir / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"Generated: {output_path}")

    def generate(self, pages):
        """
        Generate the entire site.

        Args:
            pages: List of tuples (template_name, data_file, output_file)
        """
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Generate pages
        for template_name, data_file, output_file in pages:
            self.generate_page(template_name, data_file, output_file)

        # Copy static files
        self.copy_static_files()

        print(f"\nSite generation complete! Output in: {self.output_dir}")


def main():
    """Generate site from pages.json configuration."""
    generator = StaticSiteGenerator()

    # Load pages configuration from JSON
    with open('data/pages.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Convert from dict format to tuple format
    # Format: (template_name, data_file, output_file)
    pages = [
        (page['template'], page['data'], page['output'])
        for page in config['pages']
    ]

    generator.generate(pages)


if __name__ == '__main__':
    main()
