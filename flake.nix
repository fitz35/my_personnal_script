
{
  description = "flake support my_personnal_script nixos module";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      inherit (nixpkgs.lib) genAttrs optional;
      eachSystem = f: genAttrs
        [
          "aarch64-darwin"
          "aarch64-linux"
          "x86_64-darwin"
          "x86_64-linux"
        ]
        (system: f nixpkgs.legacyPackages.${system});

      my_personnal_script =
        { pkgs, ... }:
        pkgs.stdenv.mkDerivation {
          name = "my_personnal_script_theme";
          src = "${self}";

          buildInputs = with pkgs; [ 
            rofi # menu
            python3 # python
            i3 # window manager
            i3lock  # lock screen
            kitty # terminal
            feh # wallpaper
          ];


          buildPhase = ''
            mkdir -p $out/bin;
          '';

          installPhase = ''
            cp -r ./src/* $out/bin;
            chmod +x $out/bin/my_script.sh;
          '';
        };
    in
    {
      nixosModules.default = { config, pkgs, ... }:
        let
          inherit (nixpkgs.lib) mkOption types mkIf;
        in
        {
        

          packages = eachSystem
            (pkgs: {
              default = my_personnal_script {
                inherit pkgs;
                # splash = "custom splash text";
              };
            });
        };
    }
}