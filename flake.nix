
{
  description = "flake support my_personnal_script nixos module";

  inputs.nixpkgs.url = github:NixOS/nixpkgs/nixos-unstable;

  outputs = { self, nixpkgs }: {

    packages.x86_64-linux.default =
      # Notice the reference to nixpkgs here.
      with import nixpkgs { system = "x86_64-linux"; };
      stdenv.mkDerivation {
        name = "my_personnal_script";
        src = self;
        buildPhase = "chmod +x dispatch.sh";
        installPhase = "install -t dispatch.sh";
      };

  };
}