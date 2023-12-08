# debian-rfs-stats
Calculate mean and median waiting time in days for RFS (Request for Sponsor)
bugs in Debian to be closed.

## Install

I can't publish to PyPi as new registrations are temporarily disabled, but you
can install from the [Codeberg package
registry](https://codeberg.org/Maytha8/-/packages/pypi/debian-rfs-stats) like
so:

```sh
pip install --index-url https://codeberg.org/api/packages/Maytha8/pypi/simple/ debian-rfs-stats
```

From source? This project uses Poetry, so a simple `poetry install` and `poetry
run debian-rfs-stats` should work. Use `pip install .` in the source directory
to install from source.

## Usage

Use `--help` flag for usage info.

## What is an RFS?

When someone outside of the Debian project (i.e. not a [Debian
Developer](https://wiki.debian.org/Glossary#debian-developer) nor [Debian
Maintainer](https://wiki.debian.org/Glossary#debian-maintainer)) creates a
package for a piece of software, they cannot upload their packages directly to
the official Debian archives, as only members of Debian can do so.

Instead, these people file RFS ("Request for Sponsor") reports against the
sponsorship-requests [virtual
package](https://wiki.debian.org/Glossary#virtual-package), asking for a Debian
Developer to review their work and upload the package on their behalf.

## Why?

I made this so I could see around how long I should wait for my RFS bugs in
Debian to be addressed.

## Copyright

Copyright &copy; 2023 Maytham Alsudany `<maytha8thedev@gmail.com>`

## License

MIT. See [LICENSE](./LICENSE).
