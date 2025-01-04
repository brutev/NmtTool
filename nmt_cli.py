import click
import os
import json


@click.group()
def cli():
    """CLI for managing Flutter-related tasks and utilities."""
    pass


@cli.command()
def version():
    """Check the version of the tool."""
    print("NmtTool version 0.0.1")


@cli.command()
@click.argument('project_name')
def create(project_name: str):
    """
    Create a new Flutter project with NMT structure.
    This sets up a standard directory structure for organized development.
    """
    os.system(f'flutter create {project_name}')

    # Create standard directories
    directories = [
        'lib/core',
        'lib/features',
        'lib/shared',
        'lib/config',
    ]

    for dir_path in directories:
        os.makedirs(f'{project_name}/{dir_path}', exist_ok=True)

    click.echo(f'Created NMT project: {project_name}')


@cli.command()
@click.argument('feature_name')
def feature(feature_name: str):
    """
    Generate a new feature module.
    Each module includes 'data', 'domain', and 'presentation' directories.
    """
    feature_path = f'lib/features/{feature_name}'
    subdirs = ['data', 'domain', 'presentation']

    for subdir in subdirs:
        os.makedirs(f'{feature_path}/{subdir}', exist_ok=True)

    click.echo(f'Created feature module: {feature_name}')


@cli.command()
def init():
    """
    Initialize NMT configuration.
    This creates a configuration file (nmt.json) with basic project metadata.
    """
    config = {
        'projectName': os.path.basename(os.getcwd()),
        'version': '1.0.0'
    }

    with open('nmt.json', 'w') as f:
        json.dump(config, f, indent=2)

    click.echo('Initialized NMT configuration')

@cli.command()
@click.argument('new_package_name')
def change_package_name(new_package_name: str):
    """
    Change the package name of a Flutter app.
    This updates both Android and iOS configurations.
    """
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
    if os.path.exists(ios_path):
        with open(ios_path, 'r') as f:
            content = f.read()

        content = content.replace(f'PRODUCT_BUNDLE_IDENTIFIER = {old_package_name};', f'PRODUCT_BUNDLE_IDENTIFIER = {new_package_name};')

        with open(ios_path, 'w') as f:
            f.write(content)

        click.echo(f"Updated iOS bundle identifier to '{new_package_name}'.")

    click.echo("Package name change completed. You may need to run 'flutter clean' before rebuilding the project.")

@cli.command()
def flutter_layout():
    """Generate a responsive Flutter layout template."""
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
    print("Responsive Flutter Layout Code:\n")
    print(layout_code)


if __name__ == "__main__":
    cli()
