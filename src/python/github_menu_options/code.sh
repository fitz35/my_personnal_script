cd $1

if test -e "flake.nix"; then
    
    nix develop --command bash -c "code ."
else
    code .
fi
