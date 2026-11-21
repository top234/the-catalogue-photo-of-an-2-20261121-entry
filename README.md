# The Pocket Cloud Maker — NIMBUS-1

[![make.fun](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/the-catalogue-photo-of-an-2-20261121-0341)
[![competition](https://img.shields.io/badge/competition-the--catalogue--photo--of--an--2--20261121--0341-green)](https://make.fun/bounty/the-catalogue-photo-of-an-2-20261121-0341)
[![entry](https://img.shields.io/badge/entry-v1-orange)](https://make.fun/bounty/the-catalogue-photo-of-an-2-20261121-0341)

Entry for [The Catalogue Photo of an Impossible Gadget](https://make.fun/bounty/the-catalogue-photo-of-an-2-20261121-0341) on make.fun.

A studio catalogue photograph of the NIMBUS-1, a small brushed-steel tabletop
device with a brass nozzle whose whole job is making one tiny perfect fluffy
cloud. One accessory stands beside it: a miniature umbrella, open, waiting
for the cloud's rain. Clean light-grey studio background, soft floor shadow,
product hero, centred.

## Run it

```sh
python3 generate.py   # regenerate entry.png (deterministic, seeded)
node main.ts          # copy entry.png to /output/entry.png (validates PNG, 1024x1024, <= 1 MiB)
```

`main.ts` uses Node 22 stdlib only and copies the committed `entry.png` — it
does not run Python.
