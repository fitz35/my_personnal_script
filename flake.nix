{
  description = "flake support my_personnal_script nixos module";
  
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    # Add other inputs as needed
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

      # Definition of your personal script theme package
      myPersonalScriptTheme = { pkgs, lib, ... } :
        let
          glibcLocales = pkgs.glibcLocales;
        in
        pkgs.stdenv.mkDerivation rec {
          name = "my_personnal_script_theme";
          src = self;

          build_env = with pkgs; [
            # Add run-time dependencies here
            rofi
            python3
            kitty
            feh
            i3lock-color
            xdotool # auto type  
            xclip # copy paste in command line

            sshpass
          ];

          buildInputs = with pkgs; [
            # Add build-time dependencies here
            makeWrapper # make available environment at runtime
            glibcLocales # to have locale
          ];

          buildPhase = ''
            mkdir -p $out/bin;
          '';

          installPhase = ''
            cp -r ./src/* $out/bin;
            cp $out/bin/my_script.sh $out/bin/my_script;

            # Add src directory to the Python path
            echo "export PYTHONPATH=\$PYTHONPATH:$out/bin/src" > $out/bin/my_script.pth

            # only expose my_script to the user (chmod +x)
            chmod +x $out/bin/my_script;

            wrapProgram $out/bin/my_script --prefix PATH : ${lib.makeBinPath build_env} --set LOCALE_ARCHIVE "${glibcLocales}/lib/locale/locale-archive"
          '';
        };
    in
    {
      # Package definitions for various architectures
      packages = eachSystem
        (pkgs: {
          default = myPersonalScriptTheme { inherit pkgs; inherit (pkgs) lib; };
        });
    };
}
