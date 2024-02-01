# flake.nix

{
  description = "Flake with sqlite3 in devshell";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            # SQL clients
            sqlite
            mysql
            postgresql

            # Python dependencies
            python3
            python3Packages.faker
            python3Packages.matplotlib
            python3Packages.numpy

          ];
        };
      in {
        devShell = devShell;
      }
    );
}
