{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  name = "python-shell";
  buildInputs = with pkgs; [
    python315
    python314Packages.tox
    python314Packages.setuptools
    python314Packages.virtualenv
    python314Packages.mypy
    python314Packages.types-beautifulsoup4
    python314Packages.pytest
  ];
}
