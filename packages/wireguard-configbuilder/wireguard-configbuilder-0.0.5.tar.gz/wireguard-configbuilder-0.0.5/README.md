# wg-configbuilder
Generates Wireguard server and client config from yaml

# Requirements
- Python 3.9
- Rust (builds dependencies)
- Wireguard (specifically wg binary)

# Install
```
git clone https://github.com/jhfoo/wg-configbuilder.git
./bin/install
```

# Usage
```
./bin/wg-configbuilder build <yaml file>
# drops .conf files in data/
# updates yaml file with keys
```

