
{
  description = "flake support my_personnal_script nixos module";

  
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = github:NixOS/nixpkgs/nixos-unstable;

  outputs = { self, nixpkgs, flake-utils }:

    flake-utils.lib.eachDefaultSystem (system:

      let

        pkgs = import nixpkgs { inherit system; };

        my-name = "my_personnal_script";

        my-buildInputs = with pkgs; [  ];

        my-script = (pkgs.writeScriptBin my-name (builtins.readFile ./my_script.sh)).overrideAttrs(old: {

          buildCommand = "${old.buildCommand}\n patchShebangs $out";

        });

      in rec {

        defaultPackage = packages.my-script;

        packages.my-script = pkgs.symlinkJoin {

          name = my-name;

          paths = [ my-script ] ++ my-buildInputs;

          buildInputs = [ pkgs.makeWrapper ];

          postBuild = "wrapProgram $out/bin/${my-name} --prefix PATH : $out/bin";

        };

      }

    );

}