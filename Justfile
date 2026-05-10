alias b := build
alias c := clean
alias s := serve

_default:
   @just --list

# Build the project
build:
   python generate_site.py

# Clean the output directory
clean:
   rm -rf output/*

# Server the site locally for testing
serve:
    cd output; python -m http.server 8000