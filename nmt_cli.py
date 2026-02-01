
"""
NMT CLI tool for Flutter development.
Provides commands for project creation, entity generation, layout templates, and package renaming.
"""

import click
import os
import csv
import logging
import re
import shutil
import subprocess
from typing import Dict, List

@click.group()
@click.option('--verbose', is_flag=True, help='Enable verbose logging output.')
def cli(verbose: bool):
  """
  Main entry point for the NMT CLI tool.
  """
  log_level = logging.DEBUG if verbose else logging.INFO
  logging.basicConfig(level=log_level, format='[%(levelname)s] %(message)s')


def _ensure_flutter_installed() -> None:
  """
  Ensure Flutter is available on PATH.
  """
  if shutil.which('flutter') is None:
    raise click.ClickException('Flutter is not installed or not on PATH. Run "flutter doctor" to verify.')


def _validate_project_name(project_name: str) -> None:
  """
  Validate Flutter/Dart package name conventions for project names.
  """
  pattern = r'^[a-z][a-z0-9_]*$'
  if not re.match(pattern, project_name):
    suggested = re.sub(r'[^a-z0-9_]', '_', project_name.lower()).strip('_') or 'my_app'
    raise click.ClickException(
      f'Invalid Dart package name "{project_name}". Try "{suggested}" instead.'
    )


def _validate_package_name(package_name: str) -> None:
  """
  Validate Android/iOS package name (reverse-DNS style).
  """
  pattern = r'^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$'
  if not re.match(pattern, package_name):
    suggested = package_name.lower().replace('-', '_')
    raise click.ClickException(
      f'Invalid package name "{package_name}". Use reverse-DNS like "com.example.app". '
      f'Suggested: "{suggested}".'
    )


def _read_csv_sample_row(csv_path: str) -> Dict:
  """
  Read a sample row from the CSV file and validate headers.
  """
  if not os.path.exists(csv_path):
    raise click.ClickException(f'CSV file not found: {csv_path}')

  with open(csv_path, 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    if reader.fieldnames is None:
      raise click.ClickException('CSV file has no headers. Please include a header row.')
    try:
      sample_row = next(reader)
    except StopIteration:
      raise click.ClickException('CSV file has headers but no data rows.')
  return sample_row

@cli.command()
@click.argument('project_name')
def create(project_name: str):
    """
    Create a new Flutter project with the NMT directory structure.
    Args:
        project_name (str): Name of the new Flutter project.
    """
    _ensure_flutter_installed()
    _validate_project_name(project_name)
    try:
      subprocess.run(['flutter', 'create', project_name], check=True)
    except subprocess.CalledProcessError as exc:
      raise click.ClickException(f'Flutter project creation failed with exit code {exc.returncode}.')
    directories = ['lib/core/entities', 'lib/features', 'lib/shared', 'lib/config']
    for dir_path in directories:
        os.makedirs(f'{project_name}/{dir_path}', exist_ok=True)
    click.echo(f'Created NMT project: {project_name}')

@cli.command()
@click.argument('csv_path')
@click.argument('entity_name')
def generate_entity(csv_path: str, entity_name: str):
    """
    Generate a Dart Equatable entity class from a CSV file.
    Args:
        csv_path (str): Path to the CSV file.
        entity_name (str): Name of the Dart entity to generate.
    """
    sample_row = _read_csv_sample_row(csv_path)
        
    entity_template = f'''
import 'package:equatable/equatable.dart';

class {entity_name} extends Equatable {{
  {_generate_fields(sample_row)}
  
  const {entity_name}({{
    {_generate_constructor_params(sample_row)}
  }});

  @override
  List<Object?> get props => [{_generate_props(sample_row)}];

  factory {entity_name}.fromMap(Map<String, dynamic> map) {{
    return {entity_name}(
      {_generate_from_map(sample_row)}
    );
  }}

  factory {entity_name}.fromCsv(List<String> row, List<String> headers) {{
    Map<String, dynamic> map = {{}};
    for (var i = 0; i < headers.length; i++) {{
      map[headers[i]] = row[i];
    }}
    return {entity_name}.fromMap(map);
  }}
}}
'''
    
    output_path = f'lib/core/entities/{entity_name.lower()}.dart'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write(entity_template)
    
    click.echo(f'Generated entity: {output_path}')

def _generate_fields(sample_row: Dict) -> str:
  """
  Generate Dart class fields from a sample CSV row.
  Args:
    sample_row (Dict): Example row from CSV.
  Returns:
    str: Dart fields as a string.
  """
  return '\n  '.join([f'final {_infer_type(value)} {key};' for key, value in sample_row.items()])

def _generate_constructor_params(sample_row: Dict) -> str:
  """
  Generate Dart constructor parameters from a sample CSV row.
  Args:
    sample_row (Dict): Example row from CSV.
  Returns:
    str: Constructor parameters as a string.
  """
  return '\n    '.join([f'required this.{key},' for key in sample_row.keys()])

def _generate_props(sample_row: Dict) -> str:
  """
  Generate the props list for Equatable from a sample CSV row.
  Args:
    sample_row (Dict): Example row from CSV.
  Returns:
    str: Comma-separated property names.
  """
  return ', '.join(sample_row.keys())

def _generate_from_map(sample_row: Dict) -> str:
  """
  Generate Dart fromMap factory assignments from a sample CSV row.
  Args:
    sample_row (Dict): Example row from CSV.
  Returns:
    str: Dart assignments for fromMap factory.
  """
  mappings = []
  for key, value in sample_row.items():
    if _infer_type(value) == 'int':
      mappings.append(f'{key}: int.parse(map[\'{key}\'].toString()),')
    elif _infer_type(value) == 'double':
      mappings.append(f'{key}: double.parse(map[\'{key}\'].toString()),')
    else:
      mappings.append(f'{key}: map[\'{key}\'] as {_infer_type(value)},')
  return '\n      '.join(mappings)

def _infer_type(value: str) -> str:
  """
  Infer Dart type from a CSV value.
  Args:
    value (str): Value from CSV.
  Returns:
    str: Dart type as a string.
  """
  try:
    int(value)
    return 'int'
  except ValueError:
    try:
      float(value)
      return 'double'
    except ValueError:
      if value.lower() in ['true', 'false']:
        return 'bool'
      return 'String'

@cli.command()
def version():
  """
  Print the version of the NMT tool.
  """
  click.echo("NmtTool version 0.0.1")

@cli.command()
def flutter_layout(project_name: str):
    """
    Generate a responsive Flutter layout template in the specified project.
    Args:
        project_name (str): Name of the Flutter project.
    """
    if not os.path.isdir(project_name):
      raise click.ClickException(f'Project directory not found: {project_name}')

    layout_code = """
import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Responsive Layout',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: ResponsiveLayout(),
    );
  }
}

class ResponsiveLayout extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Responsive Layout"),
      ),
      body: LayoutBuilder(
        builder: (context, constraints) {
          if (constraints.maxWidth < 600) {
            // Mobile layout
            return Center(
              child: Text(
                "Mobile Layout",
                style: TextStyle(fontSize: 20),
              ),
            );
          } else {
            // Tablet/Desktop layout
            return Center(
              child: Text(
                "Desktop Layout",
                style: TextStyle(fontSize: 30),
              ),
            );
          }
        },
      ),
    );
  }
}
    """

    # Define the output path
    output_path = os.path.join(project_name, 'lib', 'responsive_layout.dart')

    # Create the directories if they don't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write the Flutter layout code to the file
    with open(output_path, 'w') as file:
        file.write(layout_code)

    click.echo(f"Responsive Flutter Layout has been created at: {output_path}")

@cli.command()
@click.argument('new_package_name')
def change_package_name(new_package_name: str):
  """
  Change the package name of a Flutter app for both Android and iOS.
  Args:
    new_package_name (str): The new package/bundle identifier.
  """
  _validate_package_name(new_package_name)
  if not os.path.exists('pubspec.yaml'):
    click.echo("Error: This command must be run from the root of a Flutter project.")
    return

  # Update Android package name
  android_path = 'android/app'
  build_gradle_path = os.path.join(android_path, 'build.gradle')
  old_package_name = None

  if os.path.exists(build_gradle_path):
    with open(build_gradle_path, 'r') as f:
      content = f.read()
    # Extract the current applicationId
    old_package_name = next(
      (line.split('"')[1] for line in content.splitlines() if 'applicationId' in line), None
    )
    if old_package_name:
      content = content.replace(f'applicationId "{old_package_name}"', f'applicationId "{new_package_name}"')
      with open(build_gradle_path, 'w') as f:
        f.write(content)
      click.echo(f"Updated Android applicationId from '{old_package_name}' to '{new_package_name}'.")
    else:
      click.echo("Warning: Could not find 'applicationId' in build.gradle.")

  # Rename Android directories
  if old_package_name:
    old_dirs = old_package_name.split('.')
    new_dirs = new_package_name.split('.')
    base_dir = os.path.join(android_path, 'src', 'main', 'java')
    old_path = os.path.join(base_dir, *old_dirs)
    new_path = os.path.join(base_dir, *new_dirs)
    if os.path.exists(old_path):
      os.makedirs(new_path, exist_ok=True)
      for root, dirs, files in os.walk(old_path):
        for file in files:
          src = os.path.join(root, file)
          dst = os.path.join(new_path, os.path.relpath(src, old_path))
          os.makedirs(os.path.dirname(dst), exist_ok=True)
          os.rename(src, dst)
      # Clean up old directories
      for root, dirs, files in os.walk(old_path, topdown=False):
        for dir_ in dirs:
          os.rmdir(os.path.join(root, dir_))
        os.rmdir(root)
      click.echo(f"Renamed Android package directories to match '{new_package_name}'.")

  # Update iOS bundle identifier
  ios_path = 'ios/Runner.xcodeproj/project.pbxproj'
  if os.path.exists(ios_path) and old_package_name:
    with open(ios_path, 'r') as f:
      content = f.read()
    content = content.replace(f'PRODUCT_BUNDLE_IDENTIFIER = {old_package_name};', f'PRODUCT_BUNDLE_IDENTIFIER = {new_package_name};')
    with open(ios_path, 'w') as f:
      f.write(content)
    click.echo(f"Updated iOS bundle identifier to '{new_package_name}'.")

  click.echo("Package name change completed. You may need to run 'flutter clean' before rebuilding the project.")

if __name__ == '__main__':
    cli()
#python my_tool.py generate_entity ./entities.csv MyEntity


# import click
# import os
# import json


# @click.group()
# def cli():
#     """CLI for managing Flutter-related tasks and utilities."""
#     pass


# @cli.command()
# def version():
#     """Check the version of the tool."""
#     print("NmtTool version 0.0.1")


# @cli.command()
# @click.argument('project_name')
# def create(project_name: str):
#     """
#     Create a new Flutter project with NMT structure.
#     This sets up a standard directory structure for organized development.
#     """
#     os.system(f'flutter create {project_name}')

#     # Create standard directories
#     directories = [
#         'lib/core',
#         'lib/features',
#         'lib/shared',
#         'lib/config',
#     ]

#     for dir_path in directories:
#         os.makedirs(f'{project_name}/{dir_path}', exist_ok=True)

#     click.echo(f'Created NMT project: {project_name}')


# @cli.command()
# @click.argument('feature_name')
# def feature(feature_name: str):
#     """
#     Generate a new feature module.
#     Each module includes 'data', 'domain', and 'presentation' directories.
#     """
#     feature_path = f'lib/features/{feature_name}'
#     subdirs = ['data', 'domain', 'presentation']

#     for subdir in subdirs:
#         os.makedirs(f'{feature_path}/{subdir}', exist_ok=True)

#     click.echo(f'Created feature module: {feature_name}')


# @cli.command()
# def init():
#     """
#     Initialize NMT configuration.
#     This creates a configuration file (nmt.json) with basic project metadata.
#     """
#     config = {
#         'projectName': os.path.basename(os.getcwd()),
#         'version': '1.0.0'
#     }

#     with open('nmt.json', 'w') as f:
#         json.dump(config, f, indent=2)

#     click.echo('Initialized NMT configuration')

# @cli.command()
# @click.argument('new_package_name')
# def change_package_name(new_package_name: str):
#     """
#     Change the package name of a Flutter app.
#     This updates both Android and iOS configurations.
#     """
#     if not os.path.exists('pubspec.yaml'):
#         click.echo("Error: This command must be run from the root of a Flutter project.")
#         return

#     # Update Android package name
#     android_path = 'android/app'
#     build_gradle_path = os.path.join(android_path, 'build.gradle')
#     old_package_name = None

#     if os.path.exists(build_gradle_path):
#         with open(build_gradle_path, 'r') as f:
#             content = f.read()
        
#         # Extract the current applicationId
#         old_package_name = next(
#             (line.split('"')[1] for line in content.splitlines() if 'applicationId' in line), None
#         )

#         if old_package_name:
#             content = content.replace(f'applicationId "{old_package_name}"', f'applicationId "{new_package_name}"')

#             with open(build_gradle_path, 'w') as f:
#                 f.write(content)

#             click.echo(f"Updated Android applicationId from '{old_package_name}' to '{new_package_name}'.")
#         else:
#             click.echo("Warning: Could not find 'applicationId' in build.gradle.")

#     # Rename Android directories
#     if old_package_name:
#         old_dirs = old_package_name.split('.')
#         new_dirs = new_package_name.split('.')
#         base_dir = os.path.join(android_path, 'src', 'main', 'java')

#         old_path = os.path.join(base_dir, *old_dirs)
#         new_path = os.path.join(base_dir, *new_dirs)

#         if os.path.exists(old_path):
#             os.makedirs(new_path, exist_ok=True)
#             for root, dirs, files in os.walk(old_path):
#                 for file in files:
#                     src = os.path.join(root, file)
#                     dst = os.path.join(new_path, os.path.relpath(src, old_path))
#                     os.makedirs(os.path.dirname(dst), exist_ok=True)
#                     os.rename(src, dst)
#             # Clean up old directories
#             for root, dirs, files in os.walk(old_path, topdown=False):
#                 for dir_ in dirs:
#                     os.rmdir(os.path.join(root, dir_))
#                 os.rmdir(root)

#             click.echo(f"Renamed Android package directories to match '{new_package_name}'.")

#     # Update iOS bundle identifier
#     ios_path = 'ios/Runner.xcodeproj/project.pbxproj'
#     if os.path.exists(ios_path):
#         with open(ios_path, 'r') as f:
#             content = f.read()

#         content = content.replace(f'PRODUCT_BUNDLE_IDENTIFIER = {old_package_name};', f'PRODUCT_BUNDLE_IDENTIFIER = {new_package_name};')

#         with open(ios_path, 'w') as f:
#             f.write(content)

#         click.echo(f"Updated iOS bundle identifier to '{new_package_name}'.")

#     click.echo("Package name change completed. You may need to run 'flutter clean' before rebuilding the project.")

# @cli.command()
# def flutter_layout():
#     """Generate a responsive Flutter layout template."""
#     layout_code = """
# import 'package:flutter/material.dart';

# void main() {
#   runApp(MyApp());
# }

# class MyApp extends StatelessWidget {
#   @override
#   Widget build(BuildContext context) {
#     return MaterialApp(
#       title: 'Responsive Layout',
#       theme: ThemeData(primarySwatch: Colors.blue),
#       home: ResponsiveLayout(),
#     );
#   }
# }

# class ResponsiveLayout extends StatelessWidget {
#   @override
#   Widget build(BuildContext context) {
#     return Scaffold(
#       appBar: AppBar(
#         title: Text("Responsive Layout"),
#       ),
#       body: LayoutBuilder(
#         builder: (context, constraints) {
#           if (constraints.maxWidth < 600) {
#             // Mobile layout
#             return Center(
#               child: Text(
#                 "Mobile Layout",
#                 style: TextStyle(fontSize: 20),
#               ),
#             );
#           } else {
#             // Tablet/Desktop layout
#             return Center(
#               child: Text(
#                 "Desktop Layout",
#                 style: TextStyle(fontSize: 30),
#               ),
#             );
#           }
#         },
#       ),
#     );
#   }
# }
#     """
#     print("Responsive Flutter Layout Code:\n")
#     print(layout_code)


# if __name__ == "__main__":
#     cli()
