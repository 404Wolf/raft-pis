{
  description = "Raft implementation for raspberry PIs";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        name = "raftpi";
        pkgs = import nixpkgs { inherit system; };
        poetry = (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; });
      in {
        packages = {
          default = self.packages.${system}.${name};
          ${name} = poetry.mkPoetryApplication {
            projectDir = self;
            preferWheels = true;
          };
        };

        devShells = {
          default =
            pkgs.mkShell { inputsFrom = [ self.packages.${system}.${name} ]; };
          poetry = pkgs.mkShell {
            packages = [ pkgs.python312 pkgs.poetry ];
            shellHook = "poetry install ";
          };
        };
      });
}
