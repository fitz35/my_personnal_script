{
  description = "analysis of the daily uptime recorded by my_script (now in the dotfiles repository)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
  };

  outputs = { self, nixpkgs }:
    let
      inherit (nixpkgs.lib) genAttrs;

      # Generate attributes for each supported system
      eachSystem = f: genAttrs
        [
          "aarch64-darwin"
          "aarch64-linux"
          "x86_64-darwin"
          "x86_64-linux"
        ]
        (system: f nixpkgs.legacyPackages.${system});

      # python and jupyter for the notebook
      devShell = pkgs: let
        python = pkgs.python3;
        pythonPackages = with pkgs.python3Packages; [
          matplotlib
          notebook
          jupyterlab
          pip

          numpy
          seaborn
        ];
      in pkgs.mkShell {
        buildInputs = [ python ] ++ pythonPackages;

        shellHook = ''
          unset SOURCE_DATE_EPOCH
        '';
      };

    in
    {
      # Development shells for various architectures
      devShells = eachSystem (pkgs: {
        default = devShell pkgs;
      });
    };
}
