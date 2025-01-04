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
