# Uptime analysis

Statistics of the time spent on my computer, from the `~/daily_uptime.txt` files recorded by `my_script uptime` (the polybar uptime module).

> The scripts (`my_script`) moved to the [dotfiles](https://github.com/fitz35/dotfiles/tree/main/my_script) repository, built by its NixOS configuration.

| Path | Content |
|---|---|
| `daily_uptime_save/` | copies of `~/daily_uptime.txt` (one line per session : end date - duration) |
| `src/analyze/uptime_record.py` | parsing and statistics (sessions fused when they overlap, split by week day) ; run it to execute the tests |
| `src/analyze/analyze.ipynb` | the notebook (heatmap, stats) |

To open the notebook (python and jupyter from the flake, see [JUPYTER.md](./JUPYTER.md)) :

```shell
nix develop
jupyter lab
```
