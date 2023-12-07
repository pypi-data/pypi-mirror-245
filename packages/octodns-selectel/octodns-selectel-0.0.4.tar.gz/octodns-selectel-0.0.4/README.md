## Selectel DNS provider for octoDNS

An [octoDNS](https://github.com/octodns/octodns/) provider that targets [Selectel DNS](https://selectel.ru/en/services/additional/dns/).

### Installation

#### Command line

```
pip install octodns-selectel
```

#### requirements.txt/setup.py

Pinning specific versions or SHAs is recommended to avoid unplanned upgrades.

##### Versions

```
# Start with the latest versions and don't just copy what's here
octodns==0.9.17
octodns-selectel==0.0.3
```

##### SHAs

```
# Start with the latest/specific versions and don't just copy what's here
-e git+https://git@github.com/octodns/octodns.git@9da19749e28f68407a1c246dfdf65663cdc1c422#egg=octodns
-e git+https://git@github.com/octodns/octodns-selectel.git@ec9661f8b335241ae4746eea467a8509205e6a30#egg=octodns_selectel
```

### Configuration

```yaml
providers:
  selectel:
    class: octodns_selectel.SelectelProvider
    token: env/SELECTEL_TOKEN
```

### Support Information

#### Records

SelectelProvider supports A, AAAA, ALIAS, CNAME, MX, NS, SRV, SSHFP and TXT

#### Dynamic

SelectelProvider does not support dynamic records.

### Development

See the [/script/](/script/) directory for some tools to help with the development process. They generally follow the [Script to rule them all](https://github.com/github/scripts-to-rule-them-all) pattern. Most useful is `./script/bootstrap` which will create a venv and install both the runtime and development related requirements. It will also hook up a pre-commit hook that covers most of what's run by CI.
