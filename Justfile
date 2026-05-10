alias b := build
alias c := clean

_default:
   @just --list

# Build the project
build:
   python generate_site.py

# Clean the output directory
clean:
   rm -rf output/*