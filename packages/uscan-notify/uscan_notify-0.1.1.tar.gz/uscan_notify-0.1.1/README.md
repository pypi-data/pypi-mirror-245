# uscan-notify
Command line tool to notify of any outdated Debian packages by using uscan info
available from qa.d.o.

## Install

I can't publish to PyPi as new registrations are temporarily disabled, but you
can install from the Codeberg package registry like so:

```sh
pip install --index-url https://codeberg.org/api/packages/Maytha8/pypi/simple/ uscan-notify
```

**From source**

```
git clone https://codeberg.org/Maytha8/uscan-notify
cd uscan-notify

poetry install
poetry run uscan-notify --help # or

pip install .
```

## Usage

Use `--help` flag for usage info.


### Example: email notifications

Here's a bash script to send email notifications with the output (to use with
e.g. cron)

```bash
result="$(uscan-notify --db-path <packages>)"

if [[ $result ]]; then
  echo "uscan-notify has found outdated packages, below are the results:

$result" | mail -s "[uscan-notify] Outdated packages" "<your email>"
fi

```

## Why?

I wanted to setup email notifications whenever a new upstream version is released.

## Copyright

Copyright &copy; 2023 Maytham Alsudany `<maytha8thedev@gmail.com>`

## License

MIT (unless otherwise indicated). See [LICENSE](./LICENSE).
