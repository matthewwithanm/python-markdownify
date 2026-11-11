{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  name = "python-shell";
  buildInputs = with pkgs; [
    python316
    python314Packages.tox
    python314Packages.setuptools
    python314Packages.virtualenv
  ];
}
