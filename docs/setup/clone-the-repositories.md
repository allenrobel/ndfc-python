# Clone the repositories

We'll need to clone two repositories.

- [ndfc-python](https://github.com/allenrobel/ndfc-python)
- [ansible-dcnm](https://github.com/CiscoDevNet/ansible-dcnm/tree/main)

It's recommended to clone the repositories side-by-side in the directory where you keep your repositories.  We'll use `$HOME/repos` in our examples.

## `ndfc-python`

```bash
cd $HOME/repos
git clone https://github.com/allenrobel/ndfc-python.git
```

## `ansible-dcnm`

```bash
cd $HOME/repos
git clone https://github.com/CiscoDevNet/ansible-dcnm.git
```

Until relative-imports are integrated into the `ansible-dcnm` repository, you'll need to switch branches to the `develop` branch (if the branch isn't currently set to `develop`).

```bash
cd $HOME/repos/ansible-dcnm
git switch develop
```
