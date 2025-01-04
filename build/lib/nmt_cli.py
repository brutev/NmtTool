import click


@click.group()
def cli():
    """CLI for managing Flutter-related tasks and utilities."""
    pass


@cli.command()
def version():
    """Check the version of the tool."""
    print("NmtTool version 0.0.1")


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
